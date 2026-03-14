from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import func, Index
from datetime import datetime
from user import Base
import uuid

class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    category: Mapped[str | None]
    tags: Mapped[list[str]] = mapped_column(JSONB, default_factory=list)
    metadata: Mapped[dict] = mapped_column(JSONB, default_factory=dict)
    embeddings: Mapped[list[float]] = mapped_column(JSONB, default_factory=list)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_items_category", "category"),
        Index("idx_items_tags", "tags", postgresql_using="gin"),
        Index("idx_items_embeddings", "embeddings", 
               postgresql_using="ivfflat", 
               postgresql_ops={"embeddings": "vector_cosine_ops"},
               postgresql_with={"lists": 100, "probes": 10}),
        )
    
                                                 
    
