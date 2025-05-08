from fastapi import APIRouter
from services.MostViewedBooksService import MostViewedBooksService
from typing import List

router = APIRouter(prefix="/books/most-viewed", tags=["Most Viewed Books"])

@router.get("/top", response_model=List[dict])
def get_most_viewed_books():
    return MostViewedBooksService.get_top_books()