from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import func, Index, text
from datetime import datetime
import uuid

class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    event_type: Mapped[str] = mapped_column(nullable=False)  # e.g. "click", "purchase"
    action: Mapped[str] = mapped_column(nullable=False)  # e.g. "view", "like", "purchase"
    extra_data: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


    __table_args__ = (
        Index("idx_interactions_user_id", "user_id"),
        Index("idx_interactions_item_id", "item_id"),
        Index("idx_interactions_user_created", "user_id", text("created_at DESC"))
    )


