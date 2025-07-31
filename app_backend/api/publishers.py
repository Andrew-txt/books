from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app_backend.models import PublisherCreate, PublisherResponse, PublisherUpdate
from app_backend.tasks import create_publisher, update_publisher
from app_backend.utils import find_publisher_by_id
from app_backend.database import get_db


router = APIRouter(prefix="/publishers")


@router.post("", response_model=PublisherResponse)
async def create_publisher_handler(publisher_data: PublisherCreate, db: Session = Depends(get_db)):
   try:
        publisher = create_publisher(
            database=db,
            publisher_name=publisher_data.publisher_name,
            country=publisher_data.country
        )

        db.add(publisher)
        db.commit()
        return publisher
   except ValueError as e:
       db.rollback()
       raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=PublisherResponse)
async def read_publisher_handler(publisher_id: UUID, db: Session = Depends(get_db)):
    try:
        publisher = find_publisher_by_id(database=db, publisher_id=publisher_id)
        return publisher
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("", response_model=PublisherResponse)
async def update_publisher_handler(publisher_data: PublisherUpdate, db: Session = Depends(get_db)):
    try:
        publisher = update_publisher(
            database=db,
            publisher_id=publisher_data.publisher_id,
            fields_data=publisher_data.fields_data
        )

        db.commit()
        db.refresh(publisher)
        return publisher
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("")
async def delete_publisher_handler(publisher_id: UUID, db: Session = Depends(get_db)):
    try:
        publisher = find_publisher_by_id(database=db, publisher_id=publisher_id)
        db.delete(publisher)
        db.commit()
        return JSONResponse(
            {
                "message": "Publisher deleted"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))