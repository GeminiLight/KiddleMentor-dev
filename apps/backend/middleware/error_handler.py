"""
Global error handler middleware.

Catches all exceptions and returns structured error responses.
"""

import traceback
from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions import BackendException
from models import ErrorResponse


async def backend_exception_handler(
    request: Request,
    exc: BackendException
) -> JSONResponse:
    """Handle custom backend exceptions.

    Args:
        request: The request that caused the exception
        exc: The backend exception

    Returns:
        JSONResponse with error details
    """
    error_response = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors.

    Args:
        request: The request that caused the exception
        exc: The validation exception

    Returns:
        JSONResponse with validation error details
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })

    error_response = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": errors}
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions.

    Args:
        request: The request that caused the exception
        exc: The HTTP exception

    Returns:
        JSONResponse with error details
    """
    error_response = ErrorResponse(
        error_code=f"HTTP_{exc.status_code}",
        message=exc.detail,
        details={}
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions.

    Args:
        request: The request that caused the exception
        exc: The exception

    Returns:
        JSONResponse with error details
    """
    # Log the full traceback for debugging
    tb = traceback.format_exc()
    print(f"Unexpected error: {tb}")

    error_response = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
        details={"type": type(exc).__name__, "message": str(exc)}
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


def setup_error_handlers(app):
    """Setup all error handlers for the application.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(BackendException, backend_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
