from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService
from app.api.deps import get_review_service
from app.core.exceptions import BookNotFoundError, DatabaseError

router = APIRouter()


@router.get("/{book_id}/reviews", response_model=List[ReviewResponse])
async def get_book_reviews(
    book_id: int, review_service: ReviewService = Depends(get_review_service)
):
    """Get all reviews for a specific book"""
    try:
        return await review_service.get_reviews_by_book_id(book_id)
    except BookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@router.post(
    "/{book_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    book_id: int,
    review: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
):
    """Create a new review for a book"""
    try:
        return await review_service.create_review(book_id, review)
    except BookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review",
        )
