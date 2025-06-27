from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import logging

from app.database.models import Book
from app.schemas import BookCreate, BookResponse
from app.services.cache_service import CacheService
from app.core.exceptions import BookNotFoundError, DatabaseError

logger = logging.getLogger(__name__)


class BookService:
    def __init__(self, db: Session, cache: CacheService):
        self.db = db
        self.cache = cache

    async def get_all_books(self) -> List[BookResponse]:
        """Get all books with caching support"""
        try:
            # we dont need a caching, if we are getting all the books
            # # Try cache first
            # cached_books = await self.cache.get_books()
            # if cached_books:
            #     logger.info("Books retrieved from cache")
            #     return cached_books

            # logger.info("Cache miss - fetching books from database")
            books = self.db.query(Book).all()
            book_responses = [BookResponse.model_validate(book) for book in books]

            # # Cache the results
            # await self.cache.set_books(book_responses)

            return book_responses

        except Exception as e:
            logger.warning(f"Cache error: {e}. Falling back to database.")
            try:
                books = self.db.query(Book).all()
                return [BookResponse.model_validate(book) for book in books]
            except SQLAlchemyError as e:
                logger.error(f"Database error: {e}")
                raise DatabaseError("Failed to fetch books")

    async def get_book_by_id(self, book_id: int) -> BookResponse:
        """Get a book by ID"""
        try:
            book = self.db.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise BookNotFoundError(f"Book with id {book_id} not found")
            return BookResponse.model_validate(book)

        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError("Failed to fetch book")

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        """Create a new book"""
        try:
            db_book = Book(**book_data.model_dump())
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)

            # Invalidate cache
            self.cache.invalidate_books()

            logger.info(f"Created book: {db_book.title}")
            return BookResponse.model_validate(db_book)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error creating book: {e}")
            raise DatabaseError("Failed to create book")
