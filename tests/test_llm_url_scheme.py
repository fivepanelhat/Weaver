"""Unit tests for Ollama URL scheme hardening (Bandit B310 / SecOps)."""

import os
import sys

import pytest

# Ensure repo root is importable (matches other Weaver tests / CI without pip -e .)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from weaver_graph.llm import LocalSovereignLLM, _validate_ollama_base_url # noqa: E402


def test_validate_allows_http_https():
 assert _validate_ollama_base_url("http://localhost:11434") == "http://localhost:11434"
 assert _validate_ollama_base_url("https://edge.local:11434/") == "https://edge.local:11434"


def test_validate_rejects_file_and_empty():
 with pytest.raises(ValueError):
 _validate_ollama_base_url("file:///etc/passwd")
 with pytest.raises(ValueError):
 _validate_ollama_base_url("ftp://evil.example/x")
 with pytest.raises(ValueError):
 _validate_ollama_base_url("not-a-url")


def test_llm_init_rejects_bad_scheme():
 with pytest.raises(ValueError):
 LocalSovereignLLM(base_url="file:///tmp/x")
