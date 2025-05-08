from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone


class BorrowRecord(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )
    user_id: int = Field(
        sa_column_kwargs={"nullable": False},
        foreign_key="user.id"
    )
    book_id: int = Field(
        sa_column_kwargs={"nullable": False},
        foreign_key="book.id"
    )
    returned: bool = Field(
        sa_column_kwargs={"nullable": False}
    )
    borrowed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"nullable": False}
    )
    returned_at: Optional[datetime] = Field(
        default=None
    )
