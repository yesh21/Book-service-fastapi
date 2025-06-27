# Book Review Service

A comprehensive Book Review API built with FastAPI, Sqlite, and Redis caching.

## Features

- ✅ Clean and scalable code
- ✅ RESTful API with OpenAPI/Swagger documentation
- ✅ Sqlite database with SQLAlchemy ORM
- ✅ Redis caching with fallback handling
- ✅ Database migrations with Alembic
- ✅ Optimized database indexes
- ✅ Unit and integration tests
- ✅ Coverage report and CI friendliness

## API Endpoints

- `GET /books` - List all books (with caching)
- `POST /books` - Create a new book
- `GET /books/{id}/reviews` - Get reviews for a book
- `POST /books/{id}/reviews` - Create a review for a book

## Quick Start

1. **Running app(for the first time):**

   >This script automates the setup and launch of the application:
   > - Sets up the virtual environment
   > - Installs dependencies
   > - Runs `flake8` for linting
   > - Runs coverage and tests
   > - Starts the application

   ```bash
   bash run.sh
   ```

2. **(Optional) Skip installations:**
   ```bash
   bash run.sh --skip-install
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Architecture

### Database Schema
- **Books**: id, title, author, isbn, description, published_year
- **Reviews**: id, book_id (FK), reviewer_name, rating, review_text
- **Indexes**: Optimized for book-review queries

### Caching Strategy
- Redis caching for GET /books endpoint
- 5-minute TTL with automatic invalidation
- Graceful fallback to database if cache is unavailable

### Error Handling
- Comprehensive exception handling for database and cache errors
- Proper HTTP status codes and error messages
- Logging for debugging and monitoring

## Environment Variables

- `DATABASE_URL`: # Book Review Service

