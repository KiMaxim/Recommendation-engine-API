from select import select

from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.models.interaction import Interaction
from app.schemas.interactions import InteractionCreate, InteractionResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user

router = APIRouter()

VALID_EVENTS = {'view', 'like', 'purchase', 'share', 'click', 'skip'}
EVENT_WEIGHTS = {
    'view': 1,
    'like': 2,
    'purchase': 5,
    'share': 3,
    'click': 1,
    'skip': -1
}

@router.post('/interactions', response_model=list[InteractionResponse], tags=["interactions"])
async def get_interactions(payload: InteractionCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if payload.event_type not in VALID_EVENTS:
        raise HTTPException(status_code=400, detail=f'Invalid event type, MUST be one of {", ".join(VALID_EVENTS)}')
    
    interaction = Interaction(      
        user_id = current_user.id,
        item_id = payload.item_id,
        event_type = payload.event_type,
        weight_value = EVENT_WEIGHTS[payload.event_type],
        context = payload.context or {}
    )
    
    db.add(interaction)
    await db.commit()

    #Invalidate cache for this item and user
    await db.invalidate(interaction)
    return {'status': 'success', 'message': 'Interaction recorded successfully'}

@router.get('/interactions/{item_id}', response_model=list[InteractionResponse], tags=["interactions"])
async def get_item_interactions(current_user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Interaction).where(Interaction.item_id == current_user_id)
    )
    interactions = result.scalars().all()
    return interactions 
