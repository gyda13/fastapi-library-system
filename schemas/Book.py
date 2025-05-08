from pydantic import BaseModel, Field

class BookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1, max_length=50)

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    available: bool

    class Config:
        orm_mode = True
        from_attributes = True