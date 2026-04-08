from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime, timezone

class ItemCreate(BaseModel):
    """Schema for creating new items"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    metadata: dict | None = Field(None)
    tags: list[str] = Field(default_factory=list, max_length=20)

class ItemResponse(BaseModel):
    """Schema for item responses"""
    id: UUID
    title: str
    description: str | None
    metadata: dict | None
    tags: list[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Allow parsing from ORM models
        json_encoders={datetime: lambda v: v.isoformat()}  # Serialize datetimes as ISO strings
    )