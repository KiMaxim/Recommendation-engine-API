from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool 

    DATABASE_URL: str 
 
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AI_API_KEY: str
    EMBEDDING_MODEL: str 
    REDIS_HOST: str
    CACHE_TTL_SECONDS: int 

    class Config:
        env_file = ".env"
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()