import os
from sqlmodel import SQLModel, create_engine

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    from models.Book import Book
    from models.User import User
    from models.Borrow import BorrowRecord
    SQLModel.metadata.create_all(engine)