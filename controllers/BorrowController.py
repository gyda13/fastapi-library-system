from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from config.Session import get_session
from services import BorrowService
from schemas.Borrow import BorrowRequest, BorrowWithDetailsResponse, ReturnRequest, BorrowResponse
from typing import List
from utils.rate_limiter import limiter

router = APIRouter()

@router.post("/", response_model=BorrowResponse)
@limiter.limit("5/minute")
def borrow_book(request: Request, borrowRequest: BorrowRequest, session: Session = Depends(get_session)):
    return BorrowService.borrow_book(session, borrowRequest)


@router.post("/return", response_model=BorrowResponse)
def return_book(request: ReturnRequest, session: Session = Depends(get_session)):
    return BorrowService.return_book(session, request)

@router.get("/borrowed", response_model=List[BorrowWithDetailsResponse])
def list_borrowed_books(session: Session = Depends(get_session)):
    return BorrowService.get_all_borrowed_books(session)
