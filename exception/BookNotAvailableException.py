from exception.BaseException import AppException
from fastapi import status

class BookNotAvailableException(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="BOOK_NOT_AVAILABLE",
            message="The book is currently not available for borrowing."
        )