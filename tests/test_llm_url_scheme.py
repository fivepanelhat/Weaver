"""Unit tests for Ollama URL scheme hardening (Bandit B310 / SecOps)."""
import pytest
from weaver_graph.llm import _validate_ollama_base_url, LocalSovereignLLM


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
