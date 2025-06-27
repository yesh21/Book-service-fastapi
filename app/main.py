from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import logging

from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.database.connection import engine
from app.database.models import Base
from app.services.cache_service import CacheService


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


# asynchronous setup and cleanup,
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Book Review Service v1.0.0(runs while starting)")
    Base.metadata.create_all(
        bind=engine
    )  # it creates all the db tables defined in models
    yield
    # Shutdown
    logger.info("Shutting down Book Review Service(clean up)")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Book Review Service",
        description="Backend engineer assignment @ProcessVenue",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health")
    async def health_check():
        cache = CacheService()
        redis_status = "connected" if cache.redis_client else "disconnected"
        return {"status": "healthy", "version": "1.0.0", "redis": redis_status}

    return app


app = create_app()
