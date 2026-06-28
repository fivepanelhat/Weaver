import uuid
from typing import List, Dict, Any

try:
    # Prefer the user's installed splitter if available
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception:
    # Minimal fallback splitter with similar interface for environments
    # without the package
    class RecursiveCharacterTextSplitter:
        def __init__(
            self,
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        ):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_text(self, text: str) -> List[str]:
            # naive splitting: break on double-newlines into paragraphs, then
            # further into fixed-size windows
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            chunks: List[str] = []
            for p in paragraphs:
                if len(p) <= self.chunk_size:
                    chunks.append(p)
                else:
                    # windowed split with overlap
                    start = 0
                    while start < len(p):
                        end = start + self.chunk_size
                        chunks.append(p[start:end])
                        start = max(0, end - self.chunk_overlap)
            return chunks


class AgnosticDataIngestionEngine:
    """
    The ingestion funnel for the white-label Helpdesk.
    Processes raw text, chunks it semantically, and enforces multi-tenant data boundaries.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        # We set a sensible overlap so context isn't lost at the boundaries of
        # the chunks.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def chunk_and_tag_document(
        self, raw_text: str, tenant_id: str, source_id: str
    ) -> List[Dict[str, Any]]:
        """
        Takes raw document text, slices it up, and strictly binds the tenant's
        identity to every single resulting chunk.
        """
        # 1. Split the massive raw text string into manageable pieces
        raw_chunks = self.text_splitter.split_text(raw_text)
        processed_chunks: List[Dict[str, Any]] = []

        # 2. Iterate and build the secure payload for the Vector Database
        for index, chunk_text in enumerate(raw_chunks):
            # Generate a unique cryptographic ID for this specific
            # paragraph/chunk
            chunk_id = str(uuid.uuid4())

            # Assemble the exact schema we mapped out for the
            # PostgreSQL/pgvector table
            chunk_record = {
                "chunk_id": chunk_id,
                "source_id": source_id,
                "tenant_id": tenant_id,  # The absolute non-negotiable multi-tenant boundary
                "content_payload": chunk_text,
                # Metadata is useful for the AI to know where it is in the
                # document
                "metadata": {
                    "chunk_index": index,
                    "total_chunks": len(raw_chunks),
                },
            }
            processed_chunks.append(chunk_record)

        print(
            f"Processed {len(processed_chunks)} chunks for Tenant: "
            f"{tenant_id}"
        )
        return processed_chunks
