from sqlmodel import Session, select
from models.Book import Book
from typing import List, Optional

def save_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def get_book(session: Session, book_id: int) -> Optional[Book]:
    return session.get(Book, book_id)

def get_books(session: Session) -> List[Book]:
    return session.exec(select(Book)).all()

def search_books(
    session: Session,
    title: str = None,
    author: str = None,
    genre: str = None,
    limit: int = 10,
    offset: int = 0
) -> List[Book]:
    query = select(Book)
    filters = []

    if title:
        filters.append(Book.title.ilike(f"%{title}%"))
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))
    if genre:
        filters.append(Book.genre.ilike(f"%{genre}%"))

    if filters:
        query = query.where(*filters)

    query = query.limit(limit).offset(offset)

    return session.exec(query).all()

def delete_book(session: Session, book: Book):
    session.delete(book)
    session.commit()

