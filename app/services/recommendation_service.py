from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.util import await_fallback
from app.models import user, item, interaction
from app.services.ai_service import rank_with_ai
import uuid

class RecomendationService:
    async def get_collabarative_candidates(self, user_id: uuid.UUID, db: AsyncSession, limit: int = 100) -> dict:
        query = text('''
                    WITH user_items AS (
                            SELECT item_id from Interactions
                            WHERE user_id = :user_id and event_type in ('like', 'purchase')
                            ),
                        similar_users AS (
                            SELECT DISTINCT i2.user_id
                            FROM Interactions i2
                            WHERE i2.item_id IN (SELECT item_id FROM user_items)
                            AND i2.user_id != :user_id
                            AND i2.event_type in ('like', 'purchase')
                            ),
                        candidate_items AS (
                            SELECT i3.item_id, COUNT(*) as score
                            FROM interactions i3
                            WHERE i3.user_id in (SELECT user_id FROM similar_users)
                                AND i3.event_type NOT IN (SELECT item_id FROM user_items)
                                AND i3.event_type in ('like', 'purchase')
                            GROUP BY i3.item_id
                            ORDER BY score DESC
                            LIMIT :limit
                            )
                    SELECT items.*, ci.score
                    FROM candidate_items ci
                    JOIN items ON items.id = ci.item_id
                    ''')
        result = await db.execute(query, {'user_id': str(user_id), 'limit': limit})
        return [dict(row) for row in result.mappings()]
    
    async def get_semantic_candidates (self, db: AsyncSession, user_embedding: list[float], limit: int = 50) -> list[dict]:
        #Fetches candidate items based on semantic similarity using AI ranking.
        query = text('''
                    SELECT *, 1 - (embedding <=> : embedding::vector) AS similarity 
                     FROM items
                     ORDER BY embedding <=> :embedding::vector
                     LIMIT :limit
                    ''') 
        embedding_str = '[' + ','.join(map(str, user_embedding)) + ']'
        result = await db.execute(query,  {'embedding': embedding_str, 'limit': limit})
        return [dict(row) for row in result.mappings()]
    
    async def get_recommendation(self, db: AsyncSession, user_id: uuid.UUID, strategy: str = 'hybrid', top_k: int = 10) -> list[dict]:
        
        #Fetch user profile and preferences
        user = await db.get(user.User, user_id)
        user_profile = {
            'preferences': user.preferences,
            'display_name': user.display_name
        }

        #Gather candidates from both collaborative filtering and semantic similarity
        candidates = []
        if strategy in ('collaborative', 'hybrid'):
            collab = await self.get_collabarative_candidates(user_id, db, limit=100)
            candidates.extend(collab)
        if strategy in ('semantic', 'hybrid'):
            user_embedding = user.embedding
            semantic = await self.get_semantic_candidates(db, user_embedding, limit=50)
            candidates.extend(semantic)
        
        #Deduplicate candidates while preserving order
        seen, unique = set(), []
        for c in candidates:
            if c['id'] not in seen:
                seen.add(c['id'])
                unique.append(c)
        
        #AI re-ranking of candidates based on user profile and item attributes
        ranked = await rank_with_ai(user_profile, unique, top_k)
        return ranked
    



