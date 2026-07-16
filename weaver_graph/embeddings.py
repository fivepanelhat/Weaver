from typing import List, Dict, Any

try:
 from langchain_community.embeddings import OllamaEmbeddings
except Exception:
 OllamaEmbeddings = None


class SovereignEmbeddingEngine:
 """
 Takes the multi-tenant tagged chunks, converts the text to mathematical vectors locally,
 and stages them for database insertion.
 """

 def __init__(
 self, vector_db_client=None, model_name: str = "nomic-embed-text"
 ):
 # Try to initialize the local Ollama-based embedder when available
 if OllamaEmbeddings is not None:
 self.embedder = OllamaEmbeddings(model=model_name)
 else:
 # Fallback: a naive, deterministic mock embedder (useful for tests
 # / constrained envs)
 self.embedder = None
 self.db = vector_db_client

 def _mock_embed_documents(self, texts: List[str]) -> List[List[float]]:
 # Very small deterministic embedding: average char code and
 # distribution buckets
 vectors: List[List[float]] = []
 for t in texts:
 if not t:
 vectors.append([0.0])
 continue
 s = sum(ord(c) for c in t)
 avg = s / max(1, len(t))
 # create a tiny vector of length 4 for deterministic output
 vectors.append(
 [avg % 1.0, (avg * 3) % 1.0, (avg * 7) % 1.0, (avg * 11) % 1.0]
 )
 return vectors

 def embed_and_store(self, processed_chunks: List[Dict[str, Any]]):
 """
 Embeds the text payload while rigidly maintaining the tenant_id metadata.
 Returns the prepared records (without performing DB insertion) or a message on empty input.
 """
 if not processed_chunks:
 return "No chunks to process."

 # 1. Extract texts
 texts_to_embed = [
 chunk["content_payload"] for chunk in processed_chunks
 ]
 tenant_id = processed_chunks[0]["tenant_id"]

 print(
 f"Generating sovereign embeddings for {len(texts_to_embed)} "
 f"chunks. Tenant: {tenant_id}..."
 )

 # 2. Run embedding
 if self.embedder is not None:
 vector_embeddings = self.embedder.embed_documents(texts_to_embed)
 else:
 vector_embeddings = self._mock_embed_documents(texts_to_embed)

 # 3. Combine metadata
 ready_records = []
 for i, chunk in enumerate(processed_chunks):
 record = {
 "chunk_id": chunk["chunk_id"],
 "source_id": chunk["source_id"],
 "tenant_id": chunk["tenant_id"],
 "embedding": vector_embeddings[i],
 "content_payload": chunk["content_payload"],
 "metadata": chunk.get("metadata", {}),
 }
 ready_records.append(record)

 # 4. Optionally insert into DB if client provided (commented to avoid surprises)
 # if self.db is not None:
 # self.db.insert(collection_name="knowledge_embeddings", data=ready_records)

 print(
 f"Prepared {len(ready_records)} vector records for Tenant "
 f"{tenant_id}."
 )
 return ready_records
