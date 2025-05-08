from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from controllers import BookController, BorrowController, UserController, MostViewedBooksController
from exception.BaseException import AppException
from exception.ExceptionHandlers import global_exception_handler, validation_exception_handler
from utils.rate_limiter import limiter, get_user_id_or_ip

app = FastAPI(
    title="Library System API",
    description="Manage books, users, and borrowing operations.",
    version="1.0.0"
)

limiter = Limiter(key_func=get_user_id_or_ip)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppException, lambda r, e: e.as_response())
app.add_exception_handler(Exception, global_exception_handler)


app.include_router(BookController.router, prefix="/books")
app.include_router(UserController.router, prefix="/users")
app.include_router(BorrowController.router, prefix="/borrow")
app.include_router(MostViewedBooksController.router, prefix="/books/most-viewed")
