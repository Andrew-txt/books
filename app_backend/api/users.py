from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app_backend.models import UserCreate, UserResponse, UserUpdate
from app_backend.tasks import create_user, update_user, add_favorite_book_to_user
from app_backend.utils import find_user_by_id
from app_backend.database import get_db, UserFavoriteBook

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse)
async def create_user_handler(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(database=db, user_name=user_data.user_name, phone=user_data.phone)

        db.add(user)
        db.commit()
        return user
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=UserResponse)
async def read_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = find_user_by_id(database=db, user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("", response_model=UserResponse)
async def update_user_handler(user_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = update_user(database=db, user_id=user_data.user_id, new_user_name=user_data.user_name)
        db.commit()
        db.refresh(user)
        return user
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e)


@router.delete("")
async def delete_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = find_user_by_id(database=db, user_id=user_id)
        db.delete(user)
        db.commit()
        return JSONResponse(
            {
                "message": "User deleted"
            }
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


#User Favorite Book---------------------------------------
@router.post("/books")
async def add_book_to_user_handler(user_id: UUID, book_id: UUID, db: Session = Depends(get_db)):
    try:
        favorite_book = add_favorite_book_to_user(database=db, user_id=user_id, book_id=book_id)
        db.add(favorite_book)
        db.commit()
        return JSONResponse(
            {
                "message": "The book has been added to the user's favorite books list"
            }
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/books")
async def delete_favorite_book_handler(user_id: UUID, book_id: UUID, db: Session = Depends(get_db)):
    book = db.query(UserFavoriteBook).filter_by(user_id=user_id, book_id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(book)
    db.commit()
    return JSONResponse(
        {
            "message": "The book has been removed from the user's favorite books list"
        }
    )