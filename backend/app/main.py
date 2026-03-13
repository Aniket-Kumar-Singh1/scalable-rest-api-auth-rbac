"""
FastAPI application entry point.

- Registers all API v1 routers under /api/v1.
- Creates database tables on startup.
- Configures CORS middleware.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base  # noqa: F401 — ensures all models are imported
from app.db.database import engine
from app.api.api_v1.endpoints.auth_routes import router as auth_router
from app.api.api_v1.endpoints.task_routes import router as task_router
from app.utils.logger import get_logger

logger = get_logger("main")
settings = get_settings()

# Lifespan — runs on startup / shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on startup."""
    logger.info("Creating database tables …")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")
    yield
    logger.info("Application shutting down.")


# App instance

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A clean, scalable backend API built with FastAPI, PostgreSQL, and JWT authentication.",
    lifespan=lifespan,
)

# Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers — all under /api/v1

app.include_router(auth_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")


# Health check


@app.get("/", tags=["Health"])
def health_check():
    """Root health-check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
