from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    #Application
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool 

    #Databse
    DATABASE_URL: str
    POOL_SIZE: int
    MAX_OVERFLOW: int

    #Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    #AI
    AI_API_KEY: str
    EMBEDDING_MODEL: str
    MAX_TOKENS: int
    SYSTEM_INSTRUCTION: str
    MODEL_PATH: str

    #Redis/Cache
    REDIS_HOST: str
    CACHE_TTL_SECONDS: int

    class Config:
        env_file = ".env"
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()