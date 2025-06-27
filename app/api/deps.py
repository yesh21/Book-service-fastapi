from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cache_service import CacheService
from app.services.book_service import BookService
from app.services.review_service import ReviewService


def get_cache_service() -> CacheService:
    return CacheService()


def get_book_service(
    db: Session = Depends(get_db), cache: CacheService = Depends(get_cache_service)
) -> BookService:
    return BookService(db, cache)


def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db)
