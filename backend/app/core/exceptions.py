"""
Global exception handlers for FastAPI.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    """Resource not found."""
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} not found: {identifier}", 404)


class ValidationError(AppException):
    """Validation error."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, 400, details)


class AuthenticationError(AppException):
    """Authentication error."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(AppException):
    """Authorization error."""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, 403)


class ModelLoadError(AppException):
    """ML model loading error."""
    def __init__(self, model_name: str, details: str = None):
        super().__init__(f"Failed to load model '{model_name}': {details}", 503)


class InferenceError(AppException):
    """ML inference error."""
    def __init__(self, details: str = None):
        super().__init__(f"Inference failed: {details}", 500)


def setup_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(
            "Application exception",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "path": request.url.path,
                "error": exc.message,
                "details": exc.details,
                "status_code": exc.status_code,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "HTTP exception",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "path": request.url.path,
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "HTTPException",
                    "message": exc.detail,
                    "details": {},
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        return await http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            "Validation error",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "path": request.url.path,
                "errors": exc.errors(),
            },
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "type": "ValidationError",
                    "message": "Request validation failed",
                    "details": {"errors": exc.errors()},
                }
            },
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        return await validation_exception_handler(request, exc)

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.exception(
            "Database error",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "path": request.url.path,
                "error": str(exc),
            },
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "DatabaseError",
                    "message": "A database error occurred",
                    "details": {},
                }
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "path": request.url.path,
                "error": str(exc),
                "type": type(exc).__name__,
            },
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "details": {},
                }
            },
        )