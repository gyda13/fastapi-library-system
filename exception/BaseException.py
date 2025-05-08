from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime, timezone


class ErrorResponse:
    @staticmethod
    def build(code: str, message: str, details: dict = None, status_code: int = 500):
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": code,
                    "message": message,
                    "details": details,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )

class AppException(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: dict = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details

    def as_response(self):
        return ErrorResponse.build(self.code, self.message, self.details, self.status_code)

class NotFoundException(AppException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=f"{name.upper().replace(' ', '_')}_NOT_FOUND",
            message=f"{name} not found"
        )