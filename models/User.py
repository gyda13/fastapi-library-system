from sqlmodel import SQLModel, Field
from sqlalchemy import String
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )
    name: str = Field(sa_column_kwargs={"nullable": False})
    email: str = Field(sa_column_kwargs={"nullable": False})
