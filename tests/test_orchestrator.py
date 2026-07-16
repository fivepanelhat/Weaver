import os
import sys

# Ensure repo root is importable
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from weaver_graph.orchestrator import build_agnostic_helpdesk  # noqa: E402
from weaver_graph.llm import LocalSovereignLLM  # noqa: E402
from knowledge_base import (  # noqa: E402
    HashEmbeddingService,
    InMemoryKnowledgeBaseClient,
)


class MockLLM:
    def __init__(self, response: str):
        self.response = response

    def invoke(self, prompt: str) -> str:
        return self.response


class _MockDoc:
    def __init__(self, page_content):
        self.page_content = page_content


class MockVectorDBClient:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search(self, query, filter=None, k=3):
        return [d for d in self.docs][:k]


def test_graph_routes_to_fulfilment():
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "bv",
        "escalation_rules": {},
        "user_message": "normal question about hours",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    docs = [_MockDoc("policy text about store hours")]
    vdb = MockVectorDBClient(docs)
    llm = MockLLM("ROUTE: fulfilment\nREPLY: Happy to help with hours.")
    out = graph.run(state, vdb, llm)
    assert out.get("classification") == "fulfilment"
    assert any(
        "Fulfilment task complete" in s
        for s in out.get("conversation_history", [])
    )
    assert "policy text" in (out.get("retrieved_context") or "")


def test_graph_routes_to_escalation():
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "bv",
        "escalation_rules": {},
        "user_message": "this is angry and I want a refund",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    docs = [_MockDoc("policy text")]
    vdb = MockVectorDBClient(docs)
    llm = MockLLM("ROUTE: escalation\nREPLY: Connecting you now.")
    out = graph.run(state, vdb, llm)
    assert out.get("classification") == "escalation"
    assert any(
        "Ticket escalated to human support" in s
        for s in out.get("conversation_history", [])
    )


def test_graph_keyword_escalation_without_llm():
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "bv",
        "escalation_rules": {},
        "user_message": "I am angry about this refund",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    out = graph.run(state)
    assert out.get("classification") == "escalation"


def test_kb_retrieval_tenant_isolation():
    emb = HashEmbeddingService()
    kb = InMemoryKnowledgeBaseClient(emb)
    kb.add_document("tenant-a", "Tenant A secret warranty policy alpha")
    kb.add_document("tenant-b", "Tenant B secret warranty policy beta")

    hits_a = kb.query("warranty policy", "tenant-a", top_k=3)
    hits_b = kb.query("warranty policy", "tenant-b", top_k=3)

    assert hits_a and all("alpha" in h["content"] or "A" in h["content"] for h in hits_a)
    assert hits_b and all("beta" in h["content"] or "B" in h["content"] for h in hits_b)
    assert not any("beta" in h["content"] for h in hits_a)
    assert not any("alpha" in h["content"] for h in hits_b)


def test_graph_uses_kb_client_kwarg():
    emb = HashEmbeddingService()
    kb = InMemoryKnowledgeBaseClient(emb)
    kb.add_document("t1", "Returns are accepted within 30 days for unused goods.")

    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "friendly",
        "escalation_rules": {},
        "user_message": "What is your return policy?",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    out = graph.run(state, kb_client=kb, llm=MockLLM("ROUTE: fulfilment\nREPLY: Sure."))
    assert "30 days" in (out.get("retrieved_context") or "")
    assert out.get("classification") == "fulfilment"


def test_llm_fallback_deterministic():
    llm = LocalSovereignLLM(model="gemma4:e4b")
    # Force offline path by pointing at dead URL
    llm.base_url = "http://127.0.0.1:1"
    llm._core_client = None
    assert "ESCALATE" in llm.invoke("customer is angry and wants safety review").upper()
