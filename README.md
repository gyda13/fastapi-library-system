# Library FastAPI App

This is a FastAPI-based backend system for managing books, users, borrowing operations, and tracking the most viewed books using Redis.

---

## Features

- Add, update, delete, and list users and books
- Borrow and return books with availability check
- Track most viewed books via Redis

---

## Tools

- **FastAPI**
- **SQLModel** – ORM
- **PostgreSQL**
- **Redis**
- **Docker & Docker Compose** – Containerized deployment
- **Alembic** – Database migrations

---
## Containerization
This project includes a docker-compose.yml file that runs up the full application stack using containers.

**Included Services**
- app – FastAPI application (built from local Dockerfile)

- db – PostgreSQL database

- redis – In-memory data store used for tracking most viewed books

**Environment Variables**
- Environment variables are passed to the app container during build/run time:

```
environment:
  DATABASE_URL: postgresql://postgres:password@db:5432/library_db
  REDIS_HOST: redis
  REDIS_PORT: 6379
```

These values are injected into the FastAPI app and accessed via os.getenv in Python.

**Data Persistence**
Database data is persisted in Docker volumes to ensure your data is not lost when containers are stopped or removed:

```
volumes:
  db_data:
```

This volume is mounted to the Postgres container at /var/lib/postgresql/data.

## Running the App

```
docker compose up -d --build
```

This will:

- Build the FastAPI app image from Dockerfile

- Start the app on http://localhost:8080

- Expose Swagger docs at http://localhost:8080/docs

---

## Database Migration Setup

Alembic is used for managing database migrations. The `alembic/` directory and migration scripts are already included.

To apply the latest migrations after cloning the project:

```
alembic revision --autogenerate
```

```
alembic upgrade head
```


---

## Redis Usage

Redis is used to track how many times a book is viewed. View counts are stored in a sorted set under the key `book_views`, and each book is also cached individually by ID.

---

## Rate Limiting
Rate limiting is enforced using the **slowapi** middleware. This helps prevent abuse by limiting how many times specific endpoints can be called by the same user within a defined time window.

- The rate limit is applied only to the POST /borrow/ endpoint.

- The limit is set to 5 requests per minute.

- It is applied per user if the X-User-ID header is included in the request.

- If X-User-ID is not provided, the client’s IP address is used for rate limiting.

**Example Header**
To apply rate limiting per user, include the following header in your request:

```
X-User-ID: 123
```

**Exceeded Limit Response**
If the rate limit is exceeded, the API returns a response like:

```json
{
  "detail": "Rate limit exceeded: 5 per 1 minute"
}
```

---
# API Integration Guide – Library FastAPI App

This document outlines all available API endpoints, including request/response formats and possible error codes.

---

## `POST /books/`

**Description:** Add a new book to the library.

### Request Body (application/json):

```json
{
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "genre": "Architecture"
}
```

### Success Response (201 Created):

```json
{
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "genre": "Architecture",
    "available": true
}
```

---

## `GET /books/{book_id}`

**Description:** Retrieve a book by ID (also increments view count).

### Success Response (200 OK):

```json
{
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "genre": "Architecture",
    "available": true
}
```

---

## `GET /books/search`

**Description:** Search and filter books by title, author, or genre. Supports pagination.

### Query Parameters:

- `title` (optional): Filter by book title
- `author` (optional): Filter by author name
- `genre` (optional): Filter by genre
- `limit` (optional): Number of items per page (default: 10, max: 100)
- `offset` (optional): Pagination offset (default: 0)

### Example Request:

```
GET /books/search?&genre=Kubernetes&limit=5&offset=0
```

### Success Response (200 OK):

```json
[
  {
    "id": 7,
    "title": "Kubernetes Up and Running",
    "author": "Kelsey Hightower, Brendan Burns, Joe Beda",
    "genre": "Kubernetes",
    "available": true
  },
  {
    "id": 8,
    "title": "The Kubernetes Book",
    "author": "Nigel Poulton",
    "genre": "Kubernetes",
    "available": true
  }
]
```
---

## `GET /books/most-viewed/top`

**Description:** Fetch the 10 most viewed books for today with full book data (from Redis cache).

### Success Response (200 OK):

```json
[
  {
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "genre": "Architecture",
    "available": true
  },
  {
    "id": 2,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt, David Thomas",
    "genre": "Software Development",
    "available": true
  }
]

```

---

## `POST /users/`

**Description:** Create a new user.

### Request Body (application/json):

```json
{
  "name": "gyda almohaimeed",
  "email": "gydamohaimeed@gmail.com"
}
```

### Success Response (201 Created):

```json
{
    "id": 1,
    "name": "gyda almohaimeed",
    "email": "gydamohaimeed@gmail.com"
}
```

---

## `GET /users/{user_id}`

**Description:** Get user by ID.

### Success Response (200 OK):

```json
{
    "id": 1,
    "name": "gyda almohaimeed",
    "email": "gydamohaimeed@gmail.com"
}
```

---

## `GET /borrow/borrowed`

**Description:** Description: Retrieve a list of all currently borrowed books along with full user and book details.

### Success Response (200 OK):

```json
[
  {
    "id": 2,
    "borrowed_at": "2025-05-06T12:00:00Z",
    "returned_at": null,
    "user": {
      "id": 6,
      "name": "test",
      "email": "test@gmail.com"
    },
    "book": {
      "id": 2,
      "title": "Kubernetes: Up and Running",
      "author": "Brendan Burns, Joe Beda, Kelsey Hightower",
      "genre": "Kubernetes",
      "available": false
    }
  },
  {
    "id": 4,
    "borrowed_at": "2025-05-06T12:00:00Z",
    "returned_at": null,
    "user": {
      "id": 1,
      "name": "gyda almohaimeed",
      "email": "gydamohaimeed@gmail.com"
    },
    "book": {
      "id": 8,
      "title": "The Kubernetes Book",
      "author": "Nigel Poulton",
      "genre": "Kubernetes",
      "available": false
    }
  }
]
```
---

## `POST /borrow/`

**Description:** Borrow a book by user ID and book ID.

### Request Header:

```json
X-User-ID 
```

### Request Body (application/json):

```json
{
  "user_id": 1,
  "book_id": 1
}
```

### Success Response (200 OK):

```json
{
  "id": 123,
  "user_id": 1,
  "book_id": 1,
  "borrowed_at": "2025-05-06T12:00:00Z",
  "returned_at": null
}
```

---

## `POST /borrow/return`

**Description:** Return a previously borrowed book.

### Request Body (application/json):

```json
{
  "user_id": 1,
  "book_id": 1
}
```

### Success Response (200 OK):

```json
{
  "id": 123,
  "user_id": 1,
  "book_id": 1,
  "borrowed_at": "2025-05-06T12:00:00Z",
  "returned_at": "2025-05-07T12:00:00Z"
}
```

---

## Global Error Structure

All error responses follow this format:

**Not found error**
```json
{
  "success": false,
  "error": {
    "code": "BOOK_NOT_FOUND",
    "message": "Book not found",
    "details": null,
    "timestamp": "2025-05-06T20:00:00Z"
  }
}
```

**Validation error**
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Input validation failed.",
        "details": [
            {
                "type": "string_pattern_mismatch",
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "String should match pattern '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
                "input": "gydamohaimeed@gmail",
                "ctx": {
                    "pattern": "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
                }
            }
        ],
        "timestamp": "2025-05-06T20:00:00Z"
    }
}
```

### Common Error Codes

| Code                      | Message                          |
| ------------------------- | -------------------------------- |
| `BOOK_NOT_FOUND`          | Book not found with the given ID |
| `BOOK_NOT_AVAILABLE`      | Book is already borrowed         |
| `USER_NOT_FOUND`          | User not found with the given ID |
| `VALIDATION_ERROR`        | Input validation failed          |
| `INTERNAL_SERVER_ERROR`   | Unexpected server failure        |