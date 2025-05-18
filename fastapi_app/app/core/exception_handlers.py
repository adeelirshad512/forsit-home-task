from fastapi import Request
from fastapi.exceptions import RequestValidationError
from app.core.response import CustomResponse
from app.core.exceptions import CustomBusinessError
from app.core.logger import logger

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return CustomResponse(content=None, error=exc.errors(), status_code=400)

async def business_exception_handler(request: Request, exc: CustomBusinessError):
    logger.error(f"Business error: {exc.detail}")
    return CustomResponse(content=None, error=exc.detail, status_code=exc.status_code)

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return CustomResponse(
        content=None,
        error={"message": "Internal server error", "type": "INTERNAL_ERROR"},
        status_code=500
    )
