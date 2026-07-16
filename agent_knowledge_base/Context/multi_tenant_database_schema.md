# Multi-Tenant Database Architecture

## White-Label AI Helpdesk: Data Foundation

**Date:** 23 May 2026  
**Contributor:** Wayne Roberts, Coastal Alpine Tech Limited

This document defines the hierarchical database schema for the white-label AI helpdesk platform. The architecture uses a hybrid approach: PostgreSQL for relational business logic and configuration, and a vector database (Milvus or PostgreSQL `pgvector`) for semantic RAG embeddings. This design ensures strict data isolation across multiple tenant businesses while maintaining a single, agnostic Python codebase.

---

## 1. The Relational Core (PostgreSQL)

The relational database handles structured business logic and configuration, ensuring strict tenant isolation at the schema level.

### Table: `tenants`

The top-level ledger of the businesses licensing the helpdesk platform.

| Column | Type | Description |
|--------|------|-------------|
| `tenant_id` | UUID (Primary Key) | Unique identifier for the business (e.g., Taranaki plumbing store). |
| `company_name` | VARCHAR | The trading name of the business. |
| `industry` | VARCHAR | Used for baseline LLM context (e.g., "Retail", "Trades", "Agriculture"). |
| `subscription_tier` | VARCHAR | Defines rate limits and compute allocation (e.g., "Starter", "Professional", "Enterprise"). |
| `created_at` | TIMESTAMP | When the account was created. |
| `updated_at` | TIMESTAMP | Last update timestamp. |

### Table: `tenant_configs`

Runtime configuration for agnostic agents. This table injects business-specific rules into the `IntakeAgent` and `FulfilmentAgent` at execution time.

| Column | Type | Description |
|--------|------|-------------|
| `config_id` | UUID (Primary Key) | Unique ID for the configuration state. |
| `tenant_id` | UUID (Foreign Key) | Links back to `tenants` table. |
| `brand_voice` | TEXT | Persona guidelines (e.g., "Professional, concise" or "Cheeky, casual"). |
| `escalation_rules` | JSONB | Hard boundaries and thresholds (e.g., `{"max_refund": 50, "require_human_for": "angry_sentiment"}`). |
| `active_channels` | JSONB | Deployment channels (e.g., `{"web_widget": true, "email": false, "sms": true}`). |
| `custom_instructions` | TEXT | Additional context or constraints specific to the business. |
| `created_at` | TIMESTAMP | Configuration creation timestamp. |
| `updated_at` | TIMESTAMP | Last update timestamp. |

### Table: `knowledge_sources`

Inventory of raw data (PDFs, websites, FAQs) uploaded or linked by the business owner.

| Column | Type | Description |
|--------|------|-------------|
| `source_id` | UUID (Primary Key) | Unique identifier for the document. |
| `tenant_id` | UUID (Foreign Key) | Strict isolation to the owning business. |
| `source_type` | VARCHAR | "PDF", "Website_URL", "Zendesk_Export", "Google_Sheet", etc. |
| `source_name` | VARCHAR | Human-readable name (e.g., "Return Policy 2026"). |
| `source_uri` | VARCHAR | S3 bucket link, web URL, or local file path. |
| `sync_status` | VARCHAR | "Pending", "Embedded", "Failed", "Refreshing". |
| `chunk_count` | INT | Number of text chunks created from this source. |
| `last_updated` | TIMESTAMP | To ensure RAG pipeline isn't serving stale data. |
| `created_at` | TIMESTAMP | When the source was ingested. |

### Table: `interaction_logs`

Audit trail of all customer interactions for compliance, analytics, and debugging.

| Column | Type | Description |
|--------|------|-------------|
| `interaction_id` | UUID (Primary Key) | Unique identifier for the interaction. |
| `tenant_id` | UUID (Foreign Key) | Which business this interaction belongs to. |
| `customer_id` | VARCHAR | Identifier for the end customer (optional). |
| `input_message` | TEXT | The customer's original query. |
| `agent_chain` | VARCHAR | Agents involved (e.g., "IntakeAgent → FulfilmentAgent"). |
| `output_message` | TEXT | The AI-generated response. |
| `escalated` | BOOLEAN | Whether the interaction was handed to a human. |
| `timestamp` | TIMESTAMP | When the interaction occurred. |

---

## 2. The Semantic Memory (Vector Store / Milvus or pgvector)

The RAG pipeline where unstructured data is chunked, embedded, and queried for semantic similarity. Multi-tenancy is guaranteed by making `tenant_id` a mandatory partition key on every query.

### Collection: `knowledge_embeddings`

Stores vectorized text chunks from business knowledge sources.

| Field | Type | Description |
|-------|------|-------------|
| `chunk_id` | UUID (Primary Key) | Unique identifier for the text chunk. |
| `source_id` | UUID (Foreign Key) | Maps back to `knowledge_sources` table. |
| `tenant_id` | UUID (Indexed, Partition Key) | **Critical:** Mandatory partition for strict data isolation. All queries must filter by this first. |
| `embedding` | VECTOR(1536) | The mathematical representation (e.g., from text-embedding-3-small or local Ollama model). |
| `content_payload` | TEXT | The actual human-readable text returned to the LLM. |
| `metadata` | JSON | E.g., `{"page_number": 4, "topic": "shipping", "confidence": 0.95}` for precise citation. |
| `created_at` | TIMESTAMP | When the chunk was embedded. |

### Query Filter Pattern

Every vector search query must enforce the tenant partition **before** similarity computation:

```sql
SELECT * FROM knowledge_embeddings 
WHERE tenant_id = {current_tenant_id} 
ORDER BY cosine_distance(embedding, {query_vector}) 
LIMIT 5
```

This ensures that even if an attacker can trigger a vector search, they cannot retrieve data from another tenant.

---

## 3. Execution Flow: How Data Moves Through the System

When a customer sends a message through the helpdesk widget:

1. **Authentication & Tenant Resolution**
   - Chat widget sends request with `tenant_id` (or derived from API key).
   - Backend validates the `tenant_id` and establishes the tenant context.

2. **Configuration Retrieval**
   - Backend queries PostgreSQL: `SELECT * FROM tenant_configs WHERE tenant_id = current_tenant_id`.
   - System loads `brand_voice`, `escalation_rules`, `active_channels`.

3. **Intake & Vector Search**
   - `IntakeAgent` receives the customer's message.
   - Message is embedded using the same model as `knowledge_embeddings`.
   - Semantic search is triggered: `SELECT FROM knowledge_embeddings WHERE tenant_id = current_tenant_id ORDER BY similarity LIMIT 5`.
   - Retrieved chunks are ranked and passed to the LLM context.

4. **Prompt Assembly**
   - System concatenates: *(Base System Prompt) + (Tenant Config Brand Voice) + (Escalation Rules) + (Retrieved RAG Context)*.
   - Example:
     ```
     You are a helpful customer support agent for {company_name}.
     Brand voice: {brand_voice}
     Escalation threshold: {escalation_rules.anger_level}
     Relevant company knowledge:
     {retrieved_knowledge_chunks}
     Customer message: {input_message}
     ```

5. **LLM Execution & Response**
   - LLM generates response strictly within the constraints and knowledge of that tenant.
   - Response is validated against escalation rules.
   - If escalation needed, message is logged to `interaction_logs` with `escalated = true`.

6. **Audit & Storage**
   - Entire interaction is logged in `interaction_logs` for compliance and analytics.
   - Metrics are updated (token usage, response time, customer satisfaction).

---

## 4. Multi-Tenancy Security Guarantees

- **Hard Isolation:** Every query filters by `tenant_id` at the database level before any data retrieval.
- **No Shared State:** Agent state, embeddings, and configurations are never cross-tenant.
- **Audit Trail:** All interactions are logged with tenant context for compliance.
- **Configuration Override:** Each tenant can override brand voice, escalation rules, and active channels without affecting others.

---

## 5. Scaling Considerations

- **Partitioning:** As data grows, consider partitioning `interaction_logs` and `knowledge_embeddings` by `tenant_id`.
- **Vectorization Batch Jobs:** Run embedding updates as async batch jobs to avoid blocking the main API.
- **Connection Pooling:** Use connection pooling (e.g., PgBouncer) to manage concurrent tenant queries efficiently.
- **Local Vector Cache:** For sub-millisecond retrieval, cache recent embeddings in-memory per tenant.

---

## Implementation Status

- **PostgreSQL Schema:** Ready for `CREATE TABLE` execution.
- **Milvus / pgvector Setup:** Requires seed data and index tuning.
- **Python Integration:** ORM models (SQLAlchemy) to be built next.
- **Agent Code Updates:** Existing `agents.py` scaffold to be refactored with tenant-aware logic.
