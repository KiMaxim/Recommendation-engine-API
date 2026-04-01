from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import engine

settings = get_settings()

# Manage application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize resources
    yield
    # Shutdown: cleanup database connections
    await engine.dispose()

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Q&A API!"}