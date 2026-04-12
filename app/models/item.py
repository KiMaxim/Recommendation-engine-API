from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import func, Index
from datetime import datetime
from app.db.base import Base
import uuid

class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=False)
    category: Mapped[str | None] = mapped_column(nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    extra_data: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    embeddings: Mapped[list[float]] = mapped_column(JSONB, default=list)
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
    
                                                 
    
