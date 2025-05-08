from sqlmodel import Session
from exception.BookNotAvailableException import BookNotAvailableException
from exception.BookNotFoundException import BookNotFoundException
from models.Borrow import BorrowRecord
from schemas.Book import BookResponse
from schemas.Borrow import BorrowRequest, BorrowResponse, BorrowWithDetailsResponse, ReturnRequest
from schemas.User import UserResponse
from services import BookService as bookService
from repositories import BookRepo, BorrowRepo

def borrow_book(session: Session, request: BorrowRequest) -> BorrowResponse:
    book = BookRepo.get_book(session, request.book_id)
    
    if not book:
        raise BookNotFoundException()

    if not book.available:
        raise BookNotAvailableException()

    book.available = False
    BookRepo.save_book(session, book) 

    record = BorrowRecord(
        user_id=request.user_id,
        book_id=request.book_id,
        returned=False
    )
    saved_record = BorrowRepo.borrow_book(session, record)

    return BorrowResponse.model_validate(saved_record.model_dump())



def return_book(session: Session, request: ReturnRequest) -> BorrowResponse:
    book = BookRepo.get_book(session, request.book_id)
    if not book:
        raise BookNotFoundException()

    record = BorrowRepo.get_active_borrow(session, request.user_id, request.book_id)
    if not record:
        raise BookNotFoundException()

    book.available = True
    BookRepo.save_book(session, book)

    record.returned = True
    updated_record = BorrowRepo.return_book(session, record)

    return BorrowResponse.model_validate(updated_record.model_dump())


def get_all_borrowed_books(session: Session) -> list[BorrowWithDetailsResponse]:
    records = BorrowRepo.get_borrowed_books(session)
    return [
        BorrowWithDetailsResponse(
            id=borrow.id,
            borrowed_at=borrow.borrowed_at,
            returned_at=borrow.returned_at,
            user=UserResponse.model_validate(user),
            book=BookResponse.model_validate(book)
        )
        for borrow, book, user in records
    ]
