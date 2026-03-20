from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime  
from user import Base
import uuid

class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    item_ids: Mapped[list[uuid.UUID]] = mapped_column(JSON, nullable=False, default_factory=list)  
    scores: Mapped[list[float]] = mapped_column(JSON, nullable=False, default_factory=list)
    strategy: Mapped[str] = mapped_column(String, nullable=False)  # strategy of recommendation
    generated_at: Mapped[DateTime] = mapped_column(default=func.now(), nullable=False)  # the time when the recommendations were generated
    expires_at: Mapped[DateTime] = mapped_column(nullable=False)  # the time when the recommendations expire

