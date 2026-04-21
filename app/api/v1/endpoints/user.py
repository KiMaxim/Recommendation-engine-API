from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.core.dependencies import get_current_user

import uuid

router = APIRouter()

@router.get('/{user_id}', response_model=UserResponse, tags=["users"])
async def get_user(user_id: uuid.UUID = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user