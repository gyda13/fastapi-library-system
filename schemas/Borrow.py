from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from schemas.Book import BookResponse
from schemas.User import UserResponse

class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

class ReturnRequest(BaseModel):
    user_id: int
    book_id: int

class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned: bool

class BorrowWithDetailsResponse(BaseModel):
    id: int
    borrowed_at: datetime
    returned_at: Optional[datetime]
    user: UserResponse
    book: BookResponse


    class Config:
        orm_mode = True
        from_attributes = True