from pydantic import BaseModel, Field
from uuid import UUID
from pydantic_settings import BaseSettings


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    password: str = Field(..., min_length=6)



