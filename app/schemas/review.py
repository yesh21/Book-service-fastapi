from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., ge=1, le=5)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
