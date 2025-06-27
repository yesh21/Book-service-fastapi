from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas import BookCreate, BookResponse
from app.services.book_service import BookService
from app.api.deps import get_book_service
from app.core.exceptions import BookNotFoundError, DatabaseError

router = APIRouter()


@router.get("/", response_model=List[BookResponse])
async def get_books(book_service: BookService = Depends(get_book_service)):
    try:
        return await book_service.get_all_books()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {e}",
        )


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate, book_service: BookService = Depends(get_book_service)
):
    """Create a new book"""
    try:
        return await book_service.create_book(book)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {e}",
        )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    """Get a specific book by ID"""
    try:
        return await book_service.get_book_by_id(book_id)
    except BookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    except DatabaseError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
