from fastapi import APIRouter, Depends, Response, status, Query
from sqlmodel import Session
from config.Session import get_session
from services import BookService
from schemas.Book import BookRequest, BookResponse
from typing import List, Optional

router = APIRouter()


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookRequest, session: Session = Depends(get_session)):
    return BookService.add_book(session, book)

@router.get("/search", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    return BookService.search_books(session, title, author, genre, limit, offset)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, session: Session = Depends(get_session)):
    return BookService.get_book_by_id(session, book_id)

@router.get("/", response_model=List[BookResponse])
def list_books(session: Session = Depends(get_session)):
    return BookService.get_all_books(session)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookRequest, session: Session = Depends(get_session)):
    return BookService.update_book(session, book_id, book_data)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    BookService.delete_book(session, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    