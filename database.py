"""
Database Connection & Query Interface

Provides a clean interface for tenant-aware database operations.
Ensures strict tenant isolation on all queries.

Optimisations:
- Lazy engine / session factory (no connection on import)
- Optional auto schema init via WEAVER_AUTO_INIT_DB=1
- Batch embedding inserts
"""

from __future__ import annotations

import logging
import os
import uuid
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Iterable

from models import (
    init_db,
    create_all_tables,
    Tenant,
    TenantConfig,
    KnowledgeSource,
    VectorEmbedding,
    InteractionLog,
)

logger = logging.getLogger("weaver.database")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/coastal_alpine_helpdesk",
)  # pragma: allowlist secret

_engine = None
_SessionLocal = None
_tables_ready = False


def _get_engine_and_session_factory():
    """Lazy-create SQLAlchemy engine + sessionmaker."""
    global _engine, _SessionLocal
    if _engine is None or _SessionLocal is None:
        _engine, _SessionLocal = init_db(DATABASE_URL)
        logger.debug("Database engine initialised")
    return _engine, _SessionLocal


def ensure_tables() -> None:
    """Create tables if missing (idempotent)."""
    global _tables_ready
    if _tables_ready:
        return
    engine, _ = _get_engine_and_session_factory()
    create_all_tables(engine)
    _tables_ready = True
    logger.info("Database tables ensured")


class TenantAwareDB:
    """
    Wrapper class for all database operations.
    Enforces tenant isolation on every query.
    """

    def __init__(self, session):
        self.session = session

    # ========== TENANT OPERATIONS ==========

    def create_tenant(
        self,
        company_name: str,
        industry: str,
        subscription_tier: str = "Starter",
    ) -> Tenant:
        tenant = Tenant(
            company_name=company_name,
            industry=industry,
            subscription_tier=subscription_tier,
        )
        self.session.add(tenant)
        self.session.commit()
        return tenant

    def get_tenant(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        return (
            self.session.query(Tenant)
            .filter(Tenant.tenant_id == tenant_id)
            .first()
        )

    def get_tenant_by_name(self, company_name: str) -> Optional[Tenant]:
        return (
            self.session.query(Tenant)
            .filter(Tenant.company_name == company_name)
            .first()
        )

    # ========== TENANT CONFIG OPERATIONS ==========

    def set_tenant_config(
        self,
        tenant_id: uuid.UUID,
        brand_voice: str,
        escalation_rules: dict,
        active_channels: dict,
        custom_instructions: Optional[str] = None,
    ) -> TenantConfig:
        config = (
            self.session.query(TenantConfig)
            .filter(TenantConfig.tenant_id == tenant_id)
            .first()
        )

        if not config:
            config = TenantConfig(tenant_id=tenant_id)

        config.brand_voice = brand_voice
        config.escalation_rules = escalation_rules
        config.active_channels = active_channels
        config.custom_instructions = custom_instructions

        self.session.add(config)
        self.session.commit()
        return config

    def get_tenant_config(
        self, tenant_id: uuid.UUID
    ) -> Optional[TenantConfig]:
        return (
            self.session.query(TenantConfig)
            .filter(TenantConfig.tenant_id == tenant_id)
            .first()
        )

    # ========== KNOWLEDGE SOURCE OPERATIONS ==========

    def add_knowledge_source(
        self,
        tenant_id: uuid.UUID,
        source_type: str,
        source_name: str,
        source_uri: str,
    ) -> KnowledgeSource:
        source = KnowledgeSource(
            tenant_id=tenant_id,
            source_type=source_type,
            source_name=source_name,
            source_uri=source_uri,
            sync_status="Pending",
        )
        self.session.add(source)
        self.session.commit()
        return source

    def get_tenant_knowledge_sources(
        self, tenant_id: uuid.UUID, sync_status: Optional[str] = None
    ) -> List[KnowledgeSource]:
        query = self.session.query(KnowledgeSource).filter(
            KnowledgeSource.tenant_id == tenant_id
        )
        if sync_status:
            query = query.filter(KnowledgeSource.sync_status == sync_status)
        return query.all()

    def update_knowledge_source_status(
        self,
        source_id: uuid.UUID,
        tenant_id: uuid.UUID,
        sync_status: str,
        chunk_count: int = 0,
    ):
        source = (
            self.session.query(KnowledgeSource)
            .filter(
                KnowledgeSource.source_id == source_id,
                KnowledgeSource.tenant_id == tenant_id,
            )
            .first()
        )

        if source:
            source.sync_status = sync_status
            source.chunk_count = chunk_count
            self.session.commit()
        return source

    # ========== VECTOR EMBEDDING OPERATIONS ==========

    def add_vector_embedding(
        self,
        tenant_id: uuid.UUID,
        source_id: uuid.UUID,
        content_payload: str,
        metadata: Optional[dict] = None,
        embedding_vector: Optional[str] = None,
    ) -> VectorEmbedding:
        """Add a single embedding (prefer batch for bulk ingest)."""
        embedding = VectorEmbedding(
            tenant_id=tenant_id,
            source_id=source_id,
            content_payload=content_payload,
            embedding_metadata=metadata,
            embedding_vector=embedding_vector,
        )
        self.session.add(embedding)
        self.session.commit()
        return embedding

    def add_vector_embeddings_batch(
        self, records: Iterable[Dict[str, Any]]
    ) -> int:
        """
        Insert many embeddings in one transaction.

        Each record keys: tenant_id, source_id, content_payload,
        optional metadata / embedding_metadata, optional embedding_vector.
        """
        count = 0
        for rec in records:
            emb = VectorEmbedding(
                tenant_id=rec["tenant_id"],
                source_id=rec.get("source_id"),
                content_payload=rec["content_payload"],
                embedding_metadata=rec.get("metadata")
                or rec.get("embedding_metadata"),
                embedding_vector=rec.get("embedding_vector"),
            )
            self.session.add(emb)
            count += 1
        if count:
            self.session.commit()
        return count

    def get_tenant_embeddings(
        self, tenant_id: uuid.UUID
    ) -> List[VectorEmbedding]:
        return (
            self.session.query(VectorEmbedding)
            .filter(VectorEmbedding.tenant_id == tenant_id)
            .all()
        )

    def get_embeddings_by_source(
        self, source_id: uuid.UUID, tenant_id: uuid.UUID
    ) -> List[VectorEmbedding]:
        return (
            self.session.query(VectorEmbedding)
            .filter(
                VectorEmbedding.source_id == source_id,
                VectorEmbedding.tenant_id == tenant_id,
            )
            .all()
        )

    # ========== INTERACTION LOG OPERATIONS ==========

    def log_interaction(
        self,
        tenant_id: uuid.UUID,
        customer_id: str,
        input_message: str,
        output_message: Optional[str] = None,
        agent_chain: Optional[str] = None,
        escalated: bool = False,
        escalation_reason: Optional[str] = None,
    ) -> InteractionLog:
        log = InteractionLog(
            tenant_id=tenant_id,
            customer_id=customer_id,
            input_message=input_message,
            output_message=output_message,
            agent_chain=agent_chain,
            escalated=escalated,
            escalation_reason=escalation_reason,
        )
        self.session.add(log)
        self.session.commit()
        return log

    def get_tenant_interactions(
        self, tenant_id: uuid.UUID, limit: int = 100
    ) -> List[InteractionLog]:
        return (
            self.session.query(InteractionLog)
            .filter(InteractionLog.tenant_id == tenant_id)
            .order_by(InteractionLog.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_customer_interactions(
        self, tenant_id: uuid.UUID, customer_id: str
    ) -> List[InteractionLog]:
        return (
            self.session.query(InteractionLog)
            .filter(
                InteractionLog.tenant_id == tenant_id,
                InteractionLog.customer_id == customer_id,
            )
            .order_by(InteractionLog.timestamp.desc())
            .all()
        )


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.

    Usage:
        with get_db_session() as db:
            config = db.get_tenant_config(tenant_id)
    """
    _, SessionLocal = _get_engine_and_session_factory()
    session = SessionLocal()
    try:
        yield TenantAwareDB(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def initialize_database():
    """Create all tables if they don't exist."""
    ensure_tables()
    print("[OK] Database tables initialized.")


# Optional auto-init only when explicitly requested (edge-friendly default: off)
if os.getenv("WEAVER_AUTO_INIT_DB", "").lower() in ("1", "true", "yes"):
    try:
        ensure_tables()
    except Exception as e:
        logger.warning("Database auto-init skipped: %s", e)
