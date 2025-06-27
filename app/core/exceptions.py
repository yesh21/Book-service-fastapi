class BookReviewException(Exception):
    """Base exception for book review service"""

    pass


class BookNotFoundError(BookReviewException):
    """Raised when a book is not found"""

    pass


class DatabaseError(BookReviewException):
    """Raised when database operation fails"""

    pass


class CacheError(BookReviewException):
    """Raised when cache operation fails"""

    pass
