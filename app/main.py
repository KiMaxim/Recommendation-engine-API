from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import engine 

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup code: init DB, cache, etc
    yield
    #Shutdown code: close connections
    await engine.dispose()

app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Q&A API!"}