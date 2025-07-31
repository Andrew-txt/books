from pydantic import BaseModel, Field
from uuid import UUID
from typing import Any, Optional


class ORMBaseModel(BaseModel):
    class Config:
        from_attributes = True


class PublisherCreate(BaseModel):
    publisher_name: str = Field(..., min_length=3, max_length=35)
    country: str = Field(..., min_length=3, max_length=63)


class PublisherResponse(ORMBaseModel):
    publisher_id: UUID
    publisher_name: str
    country: str


class PublisherUpdate(BaseModel):
    publisher_id: UUID
    fields_data: dict[str, Any]


class AuthorCreate(BaseModel):
    author_name: str = Field(..., min_length=3, max_length=35)
    country: str = Field(..., min_length=3, max_length=63)


class AuthorResponse(ORMBaseModel):
    author_id: UUID
    author_name: str
    country: str


class AuthorUpdate(BaseModel):
    author_id: UUID
    fields_data: dict[str, Any]


class BookCreate(BaseModel):
    book_name: str = Field(..., min_length=1, max_length=63)
    genre: str = Field(..., min_length=4, max_length=63)
    publication_year: int = Field(..., gt=0, le=2025)
    author_id: UUID
    publisher_id: UUID


class BookResponse(ORMBaseModel):
    book_id: UUID
    book_name: str
    genre: str
    publication_year: int
    author_id: UUID
    publisher_id: Optional[UUID] = None


class BookUpdate(BaseModel):
    book_id: UUID
    fields_data: dict[str, Any]


class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=35)
    phone: str = Field(..., pattern=r"^\+?\d{10,20}$")


class UserResponse(ORMBaseModel):
    user_id: UUID
    user_name: str
    phone: str


class UserUpdate(BaseModel):
    user_id: UUID

    user_name: str