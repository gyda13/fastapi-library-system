from sqlmodel import SQLModel, Field
from sqlalchemy import String, Boolean, Integer
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    title: str = Field(sa_column_kwargs={"nullable": False})
    author: str = Field(sa_column_kwargs={"nullable": False})
    genre: str = Field(sa_column_kwargs={"nullable": False})
    available: bool = Field(default=True, sa_column_kwargs={"nullable": False})
