from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.item import Item
from app.schemas.item import ItemResponse
from app.core.dependencies import get_current_user, get_redis
from app.services.recommendation_service import RecommendationService
from app.models.user import User
import redis.asyncio as aioredis
import json
import hashlib

router = APIRouter()

svc = RecommendationService()


@router.get('/get_recommendations', response_model=list[ItemResponse], tags=["recommendations"])
async def get_recommendations(
    strategy: str = Query('hybrid', enum=['hybrid', 'collaborative', 'semantic']), #This query parameter allows the client to specify which recommendation strategy to use. The options are 'hybrid', 'collaborative', and 'semantic'. The default is 'hybrid'.
    top_k: int = Query(10, ge=1, le=50), #This query parameter allows the client to specify how many recommendations to return. The default is 10, and it must be between 1 and 50.
    db: AsyncSession = Depends(get_db), #This dependency provides an asynchronous database session that can be used to query the database for items and interactions.
    redis: aioredis.Redis = Depends(get_redis), #This dependency provides an asynchronous Redis client that can be used to cache recommendations and store user interactions.
    current_user: User = Depends(get_current_user)): #This dependency retrieves the currently authenticated user based on the access token provided in the request. It ensures that only authenticated users can access the recommendations endpoint.
    
    #Check Redis cache first
    cache_key = f'recs:{current_user.id}:{strategy}:{top_k}'
    try:
        cached = await redis.get(cache_key)
        if cached:
            items_data = json.loads(cached)
            return [Item(**item) for item in items_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing cache: {e}")

    try:
        result = await svc.get_recommendation(db=db, user_id=current_user.id, strategy=strategy, top_k=top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {e}")

    #Cache the recommendations in Redis for 1 hour
    try:
        await redis.set(cache_key, json.dumps([item.dict() for item in result]), ex=3600)
    except Exception as e:
        # Log cache error but don't fail the request
        print(f"Error caching recommendations: {e}")
        pass

    return result

@router.get('/get_semantic_candidates', response_model=list[ItemResponse], tags=["recommendations"])
async def get_semantic_candidates(
    db: AsyncSession = Depends(get_db), 
    user_embedding: list[float] = Query(..., description="User embedding vector for semantic similarity search (384 dimensions)", min_items=384, max_items=384), 
    redis: aioredis.Redis = Depends(get_redis)):
    
    # Use hash of embedding for cache key instead of embedding values
    embedding_hash = hashlib.md5(json.dumps(user_embedding).encode()).hexdigest()
    cache_key = f'semantic_candidates:{embedding_hash}'
    
    try:
        cached = await redis.get(cache_key)
        if cached:
            items_data = json.loads(cached)
            return [Item(**item) for item in items_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing cache: {e}")

    try:
        result = await svc.get_semantic_candidates(db=db, user_embedding=user_embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving semantic candidates: {e}")

    try:
        await redis.set(cache_key, json.dumps([item.dict() for item in result]), ex=3600)
    except Exception as e:
        # Log cache error but don't fail the request
        print(f"Error caching semantic candidates: {e}")
        pass
    return result
    
    
@router.get('/get_collaborative_candidates', response_model=list[ItemResponse], tags=["recommendations"])
async def get_collaborative_candidates(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    redis: aioredis.Redis = Depends(get_redis)):
    
    cache_key = f'collaborative_candidates:{current_user.id}'

    try:
        cached = await redis.get(cache_key)
        if cached:
            items_data = json.loads(cached)
            return [Item(**item) for item in items_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing cache: {e}")

    try:
        result = await svc.get_collaborative_candidates(db=db, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collaborative candidates: {e}")

    try:
        await redis.set(cache_key, json.dumps([item.dict() for item in result]), ex=3600)
    except Exception as e:
        # Log cache error but don't fail the request
        print(f"Error caching collaborative candidates: {e}")
        pass

    return result

