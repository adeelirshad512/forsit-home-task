from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

from app.core.exceptions import CustomBusinessError
from app.core.enums import ErrorType

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise CustomBusinessError(
            message="Invalid or missing API key",
            error_type=ErrorType.AUTHORIZATION_ERROR,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return api_key