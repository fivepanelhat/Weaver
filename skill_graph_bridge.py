"""Soft SkillGraph bridge — dependency-declared skill/agent load order (Core ≥0.5.10)."""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Mapping, Optional

logger = logging.getLogger("weaver.skill_graph")

try:
    from coastal_alpine_core import resolve_skill_order, SkillGraphError
except ImportError:  # pragma: no cover
    resolve_skill_order = None  # type: ignore
    SkillGraphError = ValueError  # type: ignore


def _local_topo(skills: Mapping[str, Mapping[str, Any]]) -> List[str]:
    """Fallback topological order when Core skill_graph is unavailable."""
    dep_map: Dict[str, List[str]] = {}
    for name, meta in skills.items():
        raw = meta.get("depends_on") or meta.get("dependencies") or []
        if isinstance(raw, str):
            raw = [raw]
        dep_map[name] = [str(x) for x in raw if str(x) in skills]
    indegree = {n: len(dep_map[n]) for n in dep_map}
    ready = sorted(n for n, d in indegree.items() if d == 0)
    order: List[str] = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for m, deps in dep_map.items():
            if n in deps and m not in order:
                indegree[m] -= 1
                if indegree[m] == 0:
                    ready.append(m)
                    ready.sort()
    if len(order) != len(skills):
        logger.warning("skill cycle or unresolved deps; using registration order")
        return list(skills.keys())
    return order


class SkillGraphBridge:
    """Null-safe skill dependency resolver for Weaver agents/skills."""

    def __init__(self, skills: Optional[Mapping[str, Mapping[str, Any]]] = None):
        self._skills: Dict[str, Dict[str, Any]] = {
            k: dict(v) for k, v in (skills or {}).items()
        }
        self.load_order: List[str] = []

    def register(self, name: str, meta: Optional[Mapping[str, Any]] = None) -> None:
        if not name:
            raise ValueError("skill name required")
        self._skills[name] = dict(meta or {})

    def resolve(
        self,
        *,
        required: Optional[Iterable[str]] = None,
        skills: Optional[Mapping[str, Mapping[str, Any]]] = None,
    ) -> List[str]:
        catalog = dict(skills) if skills is not None else self._skills
        if not catalog:
            self.load_order = []
            return []
        try:
            if resolve_skill_order is not None:
                kwargs: Dict[str, Any] = {}
                if required is not None:
                    kwargs["required"] = list(required)
                self.load_order = list(resolve_skill_order(catalog, **kwargs))
            else:
                self.load_order = _local_topo(catalog)
        except Exception as exp:
            logger.warning("Skill graph resolve failed (%s); dict order", exp)
            self.load_order = list(catalog.keys())
        return list(self.load_order)

    def validate(
        self, skills: Optional[Mapping[str, Mapping[str, Any]]] = None
    ) -> List[str]:
        return self.resolve(skills=skills)
