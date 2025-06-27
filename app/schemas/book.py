from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    description: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2024)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    description: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2024)


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
