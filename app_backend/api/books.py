from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app_backend.models import BookCreate, BookResponse, BookUpdate
from app_backend.tasks import create_book, update_book
from app_backend.utils import find_book_by_id
from app_backend.database import get_db, Publisher


router = APIRouter(prefix="/books")


@router.post("", response_model=BookResponse)
async def create_book_handler(book_data: BookCreate, db: Session = Depends(get_db)):
    try:
        book = create_book(
            database=db,
            book_name=book_data.book_name,
            genre=book_data.genre,
            publication_year=book_data.publication_year,
            author_id=book_data.author_id,
            publisher_id=book_data.publisher_id
        )

        if book_data.publisher_id is not None:
            publisher = db.get(Publisher, book_data.publisher_id)
            if publisher:
                publisher.books.append(book)

        db.add(book)
        db.commit()
        return book
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=BookResponse)
async def read_book_handler(book_id: UUID, db: Session = Depends(get_db)):
    try:
        book = find_book_by_id(database=db, book_id=book_id)
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("", response_model=BookResponse)
async def update_book_handler(book_data: BookUpdate, db: Session = Depends(get_db)):
    try:
        book = update_book(database=db, book_id=book_data.book_id, fields_data=book_data.fields_data)
        db.commit()
        db.refresh(book)
        return book
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("")
async def delete_book_handler(book_id: UUID, db: Session = Depends(get_db)):
    try:
        book = find_book_by_id(database=db, book_id=book_id)
        db.delete(book)
        db.commit()
        return JSONResponse(
            {
                "message": "Book deleted"
            }
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))