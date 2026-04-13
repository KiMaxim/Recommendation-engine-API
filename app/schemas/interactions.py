from pydantic import BaseModel

class InteractionCreate(BaseModel):
    item_id: int
    context: dict = {}
    interaction_type: str  # e.g., "view", "like", "purchase"

class InteractionResponse(BaseModel):
    id: int
    item_id: int
    user_id: int
    interaction_type: str
    timestamp: str