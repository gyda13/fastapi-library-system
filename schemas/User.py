from typing import Annotated
from pydantic import BaseModel, StringConstraints, constr

EmailStrRegex = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")]

class UserRequest(BaseModel):
    name: str
    email: EmailStrRegex

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True