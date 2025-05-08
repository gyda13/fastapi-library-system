import logging
from typing import List
from sqlmodel import Session
from models.Book import Book
from repositories import BookRepo
from exception.BookNotFoundException import BookNotFoundException
from schemas.Book import BookRequest, BookResponse
from services.MostViewedBooksService import MostViewedBooksService


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

def add_book(session: Session, book_req: BookRequest) -> BookResponse:
    book = Book(**book_req.model_dump())
    saved_book = BookRepo.save_book(session, book)
    return BookResponse.model_validate(saved_book.__dict__)

def search_books(
    session: Session,
    title: str = None,
    author: str = None,
    genre: str = None,
    limit: int = 10,
    offset: int = 0
) -> List[BookResponse]:
    books = BookRepo.search_books(session, title, author, genre, limit, offset)
    return [BookResponse.model_validate(book.model_dump()) for book in books]


def get_book_by_id(session: Session, book_id: int):
    book = BookRepo.get_book(session, book_id)

    if not book:
        logger.info(f"Book not fount: {book_id}")
        raise BookNotFoundException()
    
    book_response = BookResponse.model_validate(book.__dict__)
    MostViewedBooksService.increment_view(book_response.model_dump())
    return book_response

def get_all_books(session: Session) -> list[BookResponse]:
    records = BookRepo.get_books(session)
    return [BookResponse.model_validate(r.model_dump()) for r in records]

def update_book(session: Session, book_id: int, book_data: BookRequest):
    exist_book = BookRepo.get_book(session, book_id)

    if not exist_book:
        logger.info(f"Book not fount: {book_id}")
        raise BookNotFoundException()

    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(exist_book, key, value)

    BookRepo.save_book(session, exist_book)

    return BookResponse.model_validate(exist_book.__dict__)

def delete_book(session: Session, book_id: int):
    exist_book = BookRepo.get_book(session, book_id)

    if not exist_book:
        logger.info(f"Book not fount: {book_id}")
        raise BookNotFoundException()
    
    BookRepo.delete_book(session, exist_book)
    
