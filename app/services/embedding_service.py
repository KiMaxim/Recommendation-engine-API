from sentence_transformers import SentenceTransformer
from app.core.config import get_settings
from functools import lru_cache

settings = get_settings()


@lru_cache(typed=False, maxsize=None)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.MODEL_PATH) #load model from config


async def generate_embedding(text: str) -> list[float]:
    model = get_model()
    embeddings = model.encode(text, normalize_embeddings=True) #generate embedding using local model
    return embeddings.tolist()

