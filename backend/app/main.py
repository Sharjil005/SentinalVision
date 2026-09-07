"""
SentinalVision — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.core.exceptions import setup_exception_handlers
from app.db.session import init_db, get_db_context
from app.db.models import Base

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting SentinalVision API")
    setup_logging(settings.LOG_LEVEL)

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down SentinalVision API")


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="End-to-End AI Surveillance & Threat Detection System",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware (order matters - first added = outermost)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
setup_exception_handlers(app)


# Health check endpoint
@app.get("/api/v1/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "0.1.0",
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# API version prefix - routes will be added in Phase 11
# from app.api.v1 import analyses, auth, models
# app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
# app.include_router(analyses.router, prefix=settings.API_V1_PREFIX)
# app.include_router(models.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )