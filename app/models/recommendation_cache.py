from sqlalchemy import String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime
import uuid

class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    item_ids: Mapped[list[uuid.UUID]] = mapped_column(JSON, nullable=False, default=list)  
    scores: Mapped[list[float]] = mapped_column(JSON, nullable=False, default=list)
    strategy: Mapped[str] = mapped_column(String, nullable=False)  # strategy of recommendation
    generated_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)  # the time when the recommendations were generated
    expires_at: Mapped[datetime] = mapped_column(nullable=False)  # the time when the recommendations expire

