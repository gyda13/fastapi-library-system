from fastapi import Request
from fastapi.exceptions import RequestValidationError
from exception.BaseException import ErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ErrorResponse.build(
        code="VALIDATION_ERROR",
        message="Input validation failed.",
        details=exc.errors(),
        status_code=422
    )

async def global_exception_handler(request: Request, exc: Exception):
    return ErrorResponse.build(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        details=str(exc),
        status_code=500
    )
