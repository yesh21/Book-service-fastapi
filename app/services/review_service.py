from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from app.database.models import Book, Review
from app.schemas import ReviewCreate, ReviewResponse
from app.core.exceptions import BookNotFoundError, DatabaseError

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    async def get_reviews_by_book_id(self, book_id: int) -> List[ReviewResponse]:
        """Get all reviews for a specific book"""
        try:
            # Check if book exists
            book = self.db.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise BookNotFoundError(f"Book with id {book_id} not found")

            reviews = self.db.query(Review).filter(Review.book_id == book_id).all()
            return [ReviewResponse.model_validate(review) for review in reviews]

        except SQLAlchemyError as e:
            logger.error(f"Database error fetching reviews: {e}")
            raise DatabaseError("Failed to fetch reviews")

    async def create_review(
        self, book_id: int, review_data: ReviewCreate
    ) -> ReviewResponse:
        """Create a new review for a book"""
        try:
            # Check if book exists
            book = self.db.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise BookNotFoundError(f"Book with id {book_id} not found")

            db_review = Review(**review_data.model_dump(), book_id=book_id)
            self.db.add(db_review)
            self.db.commit()
            self.db.refresh(db_review)

            logger.info(f"Created review for book {book_id}")
            return ReviewResponse.model_validate(db_review)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error creating review: {e}")
            raise DatabaseError("Failed to create review")
