import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

class MostViewedBooksService:


    @staticmethod
    def increment_view(book: dict):
        book_id = book["id"]

        r.zincrby("book_views", 1, book_id)

        r.set(f"book:{book_id}", json.dumps(book), ex=86400)

    @staticmethod
    def get_top_books(limit: int = 10) -> list[dict]:
        top_book_ids = r.zrevrange("book_views", 0, limit - 1, withscores=True)
        result = []

        for book_id, views in top_book_ids:
            cached = r.get(f"book:{book_id}")
            if cached:
                book = json.loads(cached)
                book["views"] = int(views)
                result.append(book)

        return result
