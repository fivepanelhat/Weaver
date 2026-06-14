"""
SQLAlchemy ORM Models for Multi-Tenant Agentic Architecture

Defines the relational core (PostgreSQL) for Coastal Alpine Tech's white-label platform.
All models enforce strict tenant isolation at the database level.

Models:
- Tenant: Top-level business account
- TenantConfig: Runtime configuration (brand voice, escalation rules, channels)
- KnowledgeSource: Document/URL inventory for RAG pipeline
- InteractionLog: Audit trail of all customer interactions
- VectorEmbedding: Vector store entries (linked to KnowledgeSource)
"""

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    Integer,
    Boolean,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from datetime import datetime
import uuid
from typing import Optional

Base = declarative_base()


class Tenant(Base):
    """
    Top-level ledger of businesses licensing the helpdesk platform.
    Every interaction, configuration, and piece of knowledge is scoped to a tenant.
    """

    __tablename__ = "tenants"

    tenant_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_name = Column(String(255), nullable=False, unique=True)
    # e.g., "Retail", "Trades", "Healthcare"
    industry = Column(String(100), nullable=False)
    # e.g., "Starter", "Professional", "Enterprise"
    subscription_tier = Column(String(50), nullable=False, default="Starter")
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    configs = relationship(
        "TenantConfig", back_populates="tenant", cascade="all, delete-orphan"
    )
    knowledge_sources = relationship(
        "KnowledgeSource",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )
    interaction_logs = relationship(
        "InteractionLog", back_populates="tenant", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tenant(tenant_id={
            self.tenant_id}, company_name='{
            self.company_name}', industry='{
            self.industry}')>"


class TenantConfig(Base):
    """
    The "brain manual" for the agnostic agents.
    Stores runtime configuration injected into IntakeAgent and FulfillmentAgent.
    """

    __tablename__ = "tenant_configs"

    config_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        nullable=False,
    )
    # e.g., "Professional, concise, and helpful"
    brand_voice = Column(Text, nullable=True)
    # e.g., {"max_refund": 50, "require_human_for": "angry_sentiment"}
    escalation_rules = Column(JSONB, nullable=True)
    # e.g., {"web_widget": true, "email": false}
    active_channels = Column(JSONB, nullable=True)
    # Additional agent instructions
    custom_instructions = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="configs")

    def __repr__(self):
        return f"<TenantConfig(config_id={
            self.config_id}, tenant_id={
            self.tenant_id})>"


class KnowledgeSource(Base):
    """
    Inventory of raw data (PDFs, URLs, exports) uploaded by the business owner.
    Each source is embedded into the vector store; all chunks tagged with tenant_id for isolation.
    """

    __tablename__ = "knowledge_sources"

    source_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # "PDF", "Website_URL", "Zendesk_Export", "Google_Sheet", etc.
    source_type = Column(String(50), nullable=False)
    # e.g., "Return Policy 2026"
    source_name = Column(String(255), nullable=False)
    # S3 link, web URL, or local file path
    source_uri = Column(String(1024), nullable=False)
    # "Pending", "Embedded", "Failed", "Refreshing"
    sync_status = Column(String(50), nullable=False, default="Pending")
    # Number of chunks created from this source
    chunk_count = Column(Integer, nullable=True, default=0)
    last_updated = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="knowledge_sources")
    embeddings = relationship(
        "VectorEmbedding",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<KnowledgeSource(source_id={
            self.source_id}, tenant_id={
            self.tenant_id}, source_type='{
            self.source_type}', sync_status='{
                self.sync_status}')>"


class VectorEmbedding(Base):
    """
    Vector store entries with strict tenant isolation.
    Each chunk is tagged with tenant_id; similarity searches filter by tenant first.

    Note: The actual embeddings (VECTOR columns) are typically stored in Milvus or pgvector.
    This table tracks metadata and links chunks back to their source and tenant.
    """

    __tablename__ = "vector_embeddings"

    chunk_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("knowledge_sources.source_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tenant_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content_payload = Column(Text, nullable=False)  # The human-readable text
    # Serialized embedding (if storing in PostgreSQL; otherwise null)
    embedding_vector = Column(String, nullable=True)
    # e.g., {"page_number": 4, "topic": "shipping", "confidence": 0.95}
    embedding_metadata = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    # Relationships
    source = relationship("KnowledgeSource", back_populates="embeddings")

    def __repr__(self):
        return f"<VectorEmbedding(chunk_id={
            self.chunk_id}, tenant_id={
            self.tenant_id}, source_id={
            self.source_id})>"


class InteractionLog(Base):
    """
    Audit trail of all customer interactions.
    Used for compliance, analytics, debugging, and tenant-specific reporting.
    """

    __tablename__ = "interaction_logs"

    interaction_id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Optional identifier for end customer
    customer_id = Column(String(255), nullable=True)
    # The customer's original query
    input_message = Column(Text, nullable=False)
    # e.g., "IntakeAgent → FulfillmentAgent → ResolutionAgent"
    agent_chain = Column(String(500), nullable=True)
    output_message = Column(Text, nullable=True)  # The AI-generated response
    escalated = Column(
        Boolean, nullable=False, default=False
    )  # Whether handed to human
    escalation_reason = Column(Text, nullable=True)  # Why it was escalated
    timestamp = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, index=True
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="interaction_logs")

    def __repr__(self):
        return f"<InteractionLog(interaction_id={
            self.interaction_id}, tenant_id={
            self.tenant_id}, escalated={
            self.escalated})>"


class BranchLineageHealth(Base):
    """
    Tracks the health of active git branches against main.
    Used by the realtime engine to wake an agent when divergence is fatal.
    """

    __tablename__ = "branch_lineage_health"

    id = Column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    repository = Column(String(100), nullable=False)
    base_branch = Column(String(100), nullable=False)
    compare_branch = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # 'identical', 'ahead', 'behind', 'diverged', 'orphaned'
    common_ancestor_sha = Column(String(40), nullable=True)
    last_checked = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<BranchLineageHealth(id={self.id}, repository='{self.repository}', status='{self.status}')>"


# ============================================================================
# Database Connection & Session Factory
# ============================================================================


def init_db(database_url: Optional[str] = None) -> tuple:
    """
    Initialize the database engine and session factory.

    Args:
        database_url: PostgreSQL connection string.
                      Format: postgresql://user:password@localhost/dbname
                      If None, uses ENV variable DATABASE_URL.

    Returns:
        (engine, SessionLocal) tuple for use in the application.
    """
    if database_url is None:
        import os

        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost/coastal_alpine_helpdesk",
        )

    engine = create_engine(database_url, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, SessionLocal


def create_all_tables(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables(engine):
    """Drop all tables in the database (use with caution!)."""
    Base.metadata.drop_all(bind=engine)


# ============================================================================
# Helper Functions for Tenant-Aware Queries
# ============================================================================


def get_tenant_config(session, tenant_id: uuid.UUID) -> TenantConfig:
    """Retrieve the active configuration for a tenant."""
    return (
        session.query(TenantConfig)
        .filter(TenantConfig.tenant_id == tenant_id)
        .first()
    )


def get_tenant_knowledge(
    session, tenant_id: uuid.UUID, sync_status: str = "Embedded"
):
    """Retrieve all embedded knowledge sources for a tenant."""
    return (
        session.query(KnowledgeSource)
        .filter(
            KnowledgeSource.tenant_id == tenant_id,
            KnowledgeSource.sync_status == sync_status,
        )
        .all()
    )


def get_tenant_embeddings(session, tenant_id: uuid.UUID):
    """Retrieve all vector embeddings for a tenant (tenant-isolated query)."""
    return (
        session.query(VectorEmbedding)
        .filter(VectorEmbedding.tenant_id == tenant_id)
        .all()
    )


def log_interaction(
    session,
    tenant_id: uuid.UUID,
    customer_id: str,
    input_msg: str,
    output_msg: str,
    escalated: bool = False,
):
    """Log a customer interaction for audit and analytics."""
    log = InteractionLog(
        tenant_id=tenant_id,
        customer_id=customer_id,
        input_message=input_msg,
        output_message=output_msg,
        escalated=escalated,
    )
    session.add(log)
    session.commit()
    return log
