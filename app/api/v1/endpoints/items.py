import uuid


from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.item import Item
from app.services.embedding_service import generate_embedding
from app.schemas.item import ItemResponse, ItemCreate
from app.api.v1.router import router
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post('/create_item', response_model=ItemResponse, tags=["items"], status_code=201)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    embed_text = f"{payload.title} {payload.description or ''}"
    embedding = await generate_embedding(embed_text)
    item = Item(**payload.model_dump(), embedding=embedding, owner_id=current_user.id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.get('/{item_id}', response_model=ItemResponse, tags=["items"])
async def get_item(item_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item).where(Item.id == uuid.UUID(item_id))
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return item

@router.get('/', response_model=list[ItemResponse], tags=["items"])
async def list_items(category: str = None, tags: list[str] = None, page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_db)):
    query = select(Item)
    if category:
        query = query.where(Item.category == category)
    if tags:
        query = query.where(Item.tags.contains(tags))
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all()
    
    
