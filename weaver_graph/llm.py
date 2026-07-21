"""Local LLM wrapper: prefers Coastal-Alpine-Core, then Ollama HTTP, then deterministic fallback."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
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
    ):
        self.model = model
        self.base_url = _validate_ollama_base_url(base_url)
        self.timeout = timeout
        self._core_client = None
        self._init_core_client()

    def _init_core_client(self) -> None:
        try:
            from coastal_alpine_core import SovereignOllamaClient  # type: ignore

            self._core_client = SovereignOllamaClient(default_model=self.model)
            logger.debug("Using coastal_alpine_core.SovereignOllamaClient")
        except Exception:
            self._core_client = None

    def invoke(self, prompt: str) -> str:
        """Invoke the local LLM. Falls back to a deterministic response when offline."""
        if self._core_client is not None:
            try:
                # Core client APIs vary slightly across versions
                if hasattr(self._core_client, "chat"):
                    return str(self._core_client.chat(prompt))
                if hasattr(self._core_client, "invoke"):
                    return str(self._core_client.invoke(prompt))
                if hasattr(self._core_client, "generate"):
                    return str(self._core_client.generate(prompt))
            except Exception as e:
                logger.warning("Core Ollama client failed: %s", e)

        # Direct Ollama HTTP (stdlib only — no langchain on the hot path)
        try:
            return self._ollama_generate(prompt)
        except Exception as e:
            logger.warning("Ollama HTTP failed: %s", e)

        return self._fallback(prompt)

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
