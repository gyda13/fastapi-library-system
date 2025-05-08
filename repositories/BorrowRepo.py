from sqlmodel import Session, select
from models.Book import Book
from models.Borrow import BorrowRecord
from typing import List, Optional

from models.User import User

def borrow_book(session: Session, record: BorrowRecord) -> BorrowRecord:
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def get_active_borrow(session, user_id: int, book_id: int) -> Optional[BorrowRecord]:
        return session.exec(
            select(BorrowRecord).where(
                (BorrowRecord.user_id == user_id) &
                (BorrowRecord.book_id == book_id) &
                (BorrowRecord.returned == False)
            )
        ).first()

def return_book(session, record: BorrowRecord) -> BorrowRecord:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

def get_borrowed_books(session: Session) -> List[tuple[BorrowRecord, Book, User]]:
    stmt = (
        select(BorrowRecord, Book, User)
        .join(Book, Book.id == BorrowRecord.book_id)
        .join(User, User.id == BorrowRecord.user_id)
        .where(BorrowRecord.returned == False)
    )
    return session.exec(stmt).all()

