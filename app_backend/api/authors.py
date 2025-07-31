from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app_backend.models import AuthorCreate, AuthorResponse, AuthorUpdate
from app_backend.tasks import create_author, update_author
from app_backend.utils import find_author_by_id
from app_backend.database import get_db


router = APIRouter(prefix="/authors")


@router.post("", response_model=AuthorResponse)
async def create_author_handler(author_data: AuthorCreate, db: Session = Depends(get_db)):
    try:
        author = create_author(
            database=db,
            author_name=author_data.author_name,
            country=author_data.country
        )

        db.add(author)
        db.commit()
        return author
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=AuthorResponse)
async def read_author_handler(author_id: UUID, db: Session = Depends(get_db)):
    try:
        author = find_author_by_id(database=db, author_id=author_id)
        return author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("", response_model=AuthorResponse)
async def update_author_handler(author_data: AuthorUpdate, db: Session = Depends(get_db)):
    try:
        author = update_author(database=db, author_id=author_data.author_id, fields_data=author_data.fields_data)
        db.commit()
        db.refresh(author)
        return author
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("")
async def delete_author_handler(author_id: UUID, db: Session = Depends(get_db)):
    try:
        author = find_author_by_id(database=db, author_id=author_id)

        db.delete(author)
        db.commit()
        return JSONResponse(
            {
                "message": "Author deleted"
            }
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))