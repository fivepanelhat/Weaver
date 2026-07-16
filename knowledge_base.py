import heapq
import json
import uuid
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from models import VectorEmbedding


def serialize_embedding(embedding: Sequence[float]) -> str:
 return json.dumps([float(x) for x in embedding])


def deserialize_embedding(serialized: Optional[str]) -> Optional[List[float]]:
 if not serialized:
 return None
 try:
 decoded = json.loads(serialized)
 return [float(x) for x in decoded]
 except (ValueError, TypeError):
 return None


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
 if not a or not b or len(a) != len(b):
 return 0.0
 dot = sum(x * y for x, y in zip(a, b))
 norm_a = math.sqrt(sum(x * x for x in a))
 norm_b = math.sqrt(sum(y * y for y in b))
 if norm_a == 0 or norm_b == 0:
 return 0.0
 return dot / (norm_a * norm_b)


class EmbeddingService:
 """Base interface for text embedding services."""

 def embed(self, text: str) -> List[float]:
 raise NotImplementedError


class HashEmbeddingService(EmbeddingService):
 """Deterministic lightweight embedding service for POC and demos."""

 def embed(self, text: str) -> List[float]:
 counts = [0.0] * 64
 for ch in text.lower():
 counts[ord(ch) % len(counts)] += 1.0
 norm = math.sqrt(sum(x * x for x in counts))
 return [x / norm if norm else 0.0 for x in counts]


class KnowledgeBaseClient:
 """Tenant-aware knowledge base client abstraction."""

 def query(
 self, text: str, tenant_id: str, top_k: int = 5
 ) -> List[Dict[str, Any]]:
 raise NotImplementedError

 def add_document(
 self, tenant_id: str, content: str, metadata: Dict[str, Any] = None
 ) -> None:
 raise NotImplementedError


class InMemoryKnowledgeBaseClient(KnowledgeBaseClient):
 """Simple tenant-isolated in-memory knowledge base client."""

 def __init__(self, embedder: EmbeddingService):
 self.embedder = embedder
 self._chunks: List[Dict[str, Any]] = []

 def add_document(
 self, tenant_id: str, content: str, metadata: Dict[str, Any] = None
 ) -> None:
 self._chunks.append(
 {
 "tenant_id": tenant_id,
 "content": content,
 "metadata": metadata or {},
 "vector": self.embedder.embed(content),
 }
 )

 def query(
 self, text: str, tenant_id: str, top_k: int = 5
 ) -> List[Dict[str, Any]]:
 query_vector = self.embedder.embed(text)
 candidates: List[Tuple[float, Dict[str, Any]]] = []

 for chunk in self._chunks:
 if chunk["tenant_id"] != tenant_id:
 continue
 score = cosine_similarity(query_vector, chunk["vector"])
 candidates.append((score, chunk))

 top = heapq.nlargest(top_k, candidates, key=lambda item: item[0])
 return [
 {
 "content": chunk["content"],
 "metadata": chunk["metadata"],
 "score": score,
 }
 for score, chunk in top
 ]


class SqlAlchemyKnowledgeBaseClient(KnowledgeBaseClient):
 """DB-backed tenant-aware knowledge base client for SQLAlchemy models."""

 def __init__(self, db, embedder: EmbeddingService):
 self.db = db
 self.embedder = embedder

 def add_document(
 self, tenant_id: str, content: str, metadata: Dict[str, Any] = None
 ) -> None:
 source_id = metadata.get("source_id") if metadata else None

 # If embedder supports batch embed_and_store (sovereign engines), use
 # it
 if hasattr(self.embedder, "embed_and_store"):
 processed_chunks = [
 {
 "chunk_id": str(uuid.uuid4()),
 "source_id": source_id,
 "tenant_id": tenant_id,
 "content_payload": content,
 "metadata": metadata or {},
 }
 ]
 ready_records = self.embedder.embed_and_store(processed_chunks)
 batch: List[Dict[str, Any]] = []
 for rec in ready_records:
 embedding_vec = rec.get("embedding")
 serialized = (
 serialize_embedding(embedding_vec)
 if embedding_vec is not None
 else None
 )
 batch.append(
 {
 "tenant_id": tenant_id,
 "source_id": rec.get("source_id") or source_id,
 "content_payload": rec.get("content_payload") or content,
 "metadata": rec.get("metadata", {}) or (metadata or {}),
 "embedding_vector": serialized,
 }
 )
 if hasattr(self.db, "add_vector_embeddings_batch"):
 self.db.add_vector_embeddings_batch(batch)
 else:
 for rec in batch:
 self.db.add_vector_embedding(
 tenant_id=rec["tenant_id"],
 source_id=rec.get("source_id"),
 content_payload=rec["content_payload"],
 metadata=rec.get("metadata"),
 embedding_vector=rec.get("embedding_vector"),
 )
 return

 # Fallback: single-item embed
 self.db.add_vector_embedding(
 tenant_id=tenant_id,
 source_id=source_id,
 content_payload=content,
 metadata=metadata or {},
 embedding_vector=serialize_embedding(self.embedder.embed(content)),
 )

 def add_documents_batch(
 self,
 tenant_id: str,
 chunks: List[Dict[str, Any]],
 ) -> int:
 """
 Embed and store many chunks with a single DB transaction when supported.

 Each chunk: {"content": str, "metadata": dict?, "source_id": ...?}
 """
 if not chunks:
 return 0

 records_for_db: List[Dict[str, Any]] = []
 for ch in chunks:
 content = ch.get("content") or ch.get("content_payload") or ""
 meta = ch.get("metadata") or {}
 source_id = ch.get("source_id") or meta.get("source_id")
 emb = self.embedder.embed(content)
 records_for_db.append(
 {
 "tenant_id": tenant_id,
 "source_id": source_id,
 "content_payload": content,
 "metadata": meta,
 "embedding_vector": serialize_embedding(emb),
 }
 )

 if hasattr(self.db, "add_vector_embeddings_batch"):
 return self.db.add_vector_embeddings_batch(records_for_db)

 for rec in records_for_db:
 self.db.add_vector_embedding(
 tenant_id=rec["tenant_id"],
 source_id=rec.get("source_id"),
 content_payload=rec["content_payload"],
 metadata=rec.get("metadata"),
 embedding_vector=rec.get("embedding_vector"),
 )
 return len(records_for_db)

 def query(
 self, text: str, tenant_id: str, top_k: int = 5
 ) -> List[Dict[str, Any]]:
 query_vector = self.embedder.embed(text)
 rows = self.db.get_tenant_embeddings(tenant_id)
 scored: List[Tuple[float, VectorEmbedding]] = []

 # Single-pass score; avoid re-deserializing in sort key
 for row in rows:
 embedding = deserialize_embedding(row.embedding_vector)
 if embedding is None:
 continue
 score = cosine_similarity(query_vector, embedding)
 if score > 0:
 scored.append((score, row))

 top = heapq.nlargest(top_k, scored, key=lambda item: item[0])
 return [
 {
 "content": row.content_payload,
 "metadata": row.embedding_metadata,
 "score": score,
 }
 for score, row in top
 ]
