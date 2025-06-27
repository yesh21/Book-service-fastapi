from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, index=True)
    description = Column(Text)
    published_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    reviews = relationship(
        "Review", back_populates="book", cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reviewer_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    book = relationship("Book", back_populates="reviews")

    # Optimized indexes for review queries
    __table_args__ = (
        Index("idx_reviews_book_id", "book_id"),
        Index("idx_reviews_book_rating", "book_id", "rating"),
    )
