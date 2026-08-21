"""Local LLM wrapper: prefers Core get_provider, then SovereignOllamaClient, then HTTP, then fallback.

Sprint A Phase 2 — soft provider seam.
Optional llm_call SessionEvents when event_store + session_id are attached.
CAT: local-first, http(s) only, deterministic offline fallback; no secrets in payloads.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from typing import Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger("weaver.llm")

# Stack-standard default for RPi 5 16GB edge nodes
DEFAULT_MODEL = os.getenv("WEAVER_LLM_MODEL", "gemma4:e4b")
DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
_ALLOWED_SCHEMES = frozenset({"http", "https"})


def _validate_ollama_base_url(base_url: str) -> str:
    """Ensure Ollama base URL uses only http(s) before any urllib open (Bandit B310)."""
    cleaned = (base_url or "").strip().rstrip("/")
    parsed = urlparse(cleaned)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(
            f"Unsupported Ollama URL scheme {parsed.scheme!r}; only http/https allowed"
        )
    if not parsed.netloc:
        raise ValueError("Ollama base URL must include a host")
    return cleaned


class LocalSovereignLLM:
    """Thin local LLM client suitable for edge routing / helpdesk replies."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_OLLAMA_URL,
        timeout: int = 60,
        profile: str | None = None,
        event_store: Any | None = None,
        session_id: str | None = None,
        tenant_id: str | None = None,
    ):
        self.model = model
        self.base_url = _validate_ollama_base_url(base_url)
        self.timeout = timeout
        self.profile = profile or os.getenv("WEAVER_LLM_PROFILE", "edge-default")
        self.event_store = event_store
        self.session_id = session_id
        self.tenant_id = tenant_id
        self._core_client = None
        self._init_core_client()

    def bind_session(
        self,
        *,
        session_id: str,
        event_store: Any | None = None,
        tenant_id: str | None = None,
    ) -> "LocalSovereignLLM":
        """Attach SessionEvent context for llm_call emits (returns self)."""
        self.session_id = session_id
        if event_store is not None:
            self.event_store = event_store
        if tenant_id is not None:
            self.tenant_id = tenant_id
        return self

    def _emit_llm_call(
        self,
        *,
        transport: str,
        outcome: str,
        latency_seconds: float,
        prompt_chars: int,
        response_chars: int = 0,
    ) -> None:
        if self.event_store is None or not self.session_id:
            return
        try:
            self.event_store.emit(
                session_id=self.session_id,
                event_type="llm_call",
                actor="llm",
                tenant_id=self.tenant_id,
                payload={
                    "model": self.model,
                    "profile": self.profile,
                    "transport": transport,
                    "prompt_chars": prompt_chars,
                    "response_chars": response_chars,
                    "latency_ms": int(latency_seconds * 1000),
                },
                outcome=outcome,
            )
        except Exception as exc:
            logger.debug("llm_call SessionEvent failed: %s", exc)

    def _init_core_client(self) -> None:
        """Prefer Core provider registry (0.5.8+); fall back to SovereignOllamaClient."""
        # 1) Sprint A Phase 2 seam: get_provider + profile
        try:
            from coastal_alpine_core import get_provider  # type: ignore

            self._core_client = get_provider(
                "ollama",
                profile=self.profile,
                host=self.base_url,
                default_model=self.model,
                timeout=float(self.timeout),
            )
            logger.debug("Using coastal_alpine_core.get_provider(profile=%s)", self.profile)
            return
        except Exception as e:
            logger.debug("get_provider unavailable: %s", e)

        # 2) Legacy Core client (pre-0.5.8)
        try:
            from coastal_alpine_core import SovereignOllamaClient  # type: ignore

            self._core_client = SovereignOllamaClient(
                host=self.base_url,
                default_model=self.model,
                timeout=float(self.timeout),
            )
            logger.debug("Using coastal_alpine_core.SovereignOllamaClient")
        except Exception:
            self._core_client = None

    def invoke(self, prompt: str) -> str:
        """Invoke the local LLM. Falls back to a deterministic response when offline."""
        prompt_chars = len(prompt or "")
        t0 = time.perf_counter()

        if self._core_client is not None:
            try:
                if hasattr(self._core_client, "chat"):
                    text = str(self._core_client.chat(prompt))
                elif hasattr(self._core_client, "invoke"):
                    text = str(self._core_client.invoke(prompt))
                elif hasattr(self._core_client, "generate"):
                    result = self._core_client.generate(prompt)
                    if isinstance(result, dict):
                        text = str(result.get("response", result))
                    else:
                        text = str(result)
                else:
                    text = None
                if text is not None:
                    self._emit_llm_call(
                        transport="core_provider",
                        outcome="success",
                        latency_seconds=time.perf_counter() - t0,
                        prompt_chars=prompt_chars,
                        response_chars=len(text),
                    )
                    return text
            except Exception as e:
                logger.warning("Core Ollama client failed: %s", e)

        # Direct Ollama HTTP (stdlib only — no langchain on the hot path)
        try:
            text = self._ollama_generate(prompt)
            self._emit_llm_call(
                transport="ollama_http",
                outcome="success",
                latency_seconds=time.perf_counter() - t0,
                prompt_chars=prompt_chars,
                response_chars=len(text),
            )
            return text
        except Exception as e:
            logger.warning("Ollama HTTP failed: %s", e)

        text = self._fallback(prompt)
        self._emit_llm_call(
            transport="fallback",
            outcome="fallback",
            latency_seconds=time.perf_counter() - t0,
            prompt_chars=prompt_chars,
            response_chars=len(text),
        )
        return text

    def _ollama_generate(self, prompt: str) -> str:
        # Re-validate at call time so base_url cannot be swapped to file:/ etc.
        base = _validate_ollama_base_url(self.base_url)
        url = f"{base}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 256},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        # Scheme already enforced to http/https by _validate_ollama_base_url
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310
            body = json.loads(resp.read().decode("utf-8"))
        text = body.get("response") or body.get("message", {}).get("content", "")
        if not text:
            raise ValueError("Empty Ollama response")
        return str(text).strip()

    @staticmethod
    def _fallback(prompt: str) -> str:
        lower = prompt.lower()
        if any(k in lower for k in ("anger", "angry", "safety", "escalate", "refund", "lawyer")):
            return "ESCALATE"
        return "CONTINUE: I can help using our local policy documents."
