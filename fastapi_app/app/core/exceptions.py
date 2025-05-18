from typing import Any, Dict, List

from app.core.enums import ErrorType
from fastapi import HTTPException


class CustomValidationError(HTTPException):
    def __init__(self, errors: List[Dict[str, Any]]):
        error_messages = []
        for error in errors:
            field = ".".join(str(loc) for loc in error["loc"])
            msg = f"{field}: {error['msg']}"
            error_messages.append(msg)
        detail = {
            "message": "; ".join(error_messages),
            "errorType": ErrorType.VALIDATION_ERROR
        }
        super().__init__(status_code=400, detail=detail)

class CustomBusinessError(HTTPException):
    def __init__(self, message: str, error_type: ErrorType, status_code: int = 400):
        detail = {"message": message, "errorType": error_type}
        super().__init__(status_code=status_code, detail=detail)
