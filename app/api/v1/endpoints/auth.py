from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, hash_password, create_access_token, decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate

router = APIRouter()

@router.post('/register', status_code = 201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    #Check if email exists
    existing = await db.execute(select(User).where(User.email == payload.email)) #cursor object
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(
        email = payload.email,
        hashed_password = hash_password(payload.password),
        display_name = payload.display_name
    )
    db.add(user)
    await db.commit()
    return {'id': user.id, 'email': user.email, 'display_name': user.display_name}


@router.post('/login', status_code = 200, response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form.username)) #CursorResult
    user = result.scalar_one_or_none()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect email or password')

    token = create_access_token({'sub': user.id})
    return {'access_token': token, 'token_type': 'bearer'}
