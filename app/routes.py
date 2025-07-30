from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import uvicorn

from app.tasks import *
from app.database import get_db
from app.models import *
from app.utils import find_publisher_by_id


app = FastAPI()


#Publisher---------------------------------------------------------
@app.post("/publishers", response_model=PublisherResponse)
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


@app.get("/publishers", response_model=PublisherResponse)
async def read_publisher_handler(publisher_id: UUID, db: Session = Depends(get_db)):
    try:
        publisher = find_publisher_by_id(database=db, publisher_id=publisher_id)
        return publisher
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/publishers", response_model=PublisherResponse)
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


@app.delete("/publishers")
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


#Author---------------------------------------------------------
@app.post("/authors", response_model=AuthorResponse)
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


@app.get("/authors", response_model=AuthorResponse)
async def read_author_handler(author_id: UUID, db: Session = Depends(get_db)):
    try:
        author = find_author_by_id(database=db, author_id=author_id)
        return author
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/authors", response_model=AuthorResponse)
async def update_author_handler(author_data: AuthorUpdate, db: Session = Depends(get_db)):
    try:
        author = update_author(database=db, author_id=author_data.author_id, fields_data=author_data.fields_data)
        db.commit()
        db.refresh(author)
        return author
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/authors")
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


#Books---------------------------------------------------------
@app.post("/books", response_model=BookResponse)
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


@app.get("/books", response_model=BookResponse)
async def read_book_handler(book_id: UUID, db: Session = Depends(get_db)):
    try:
        book = find_book_by_id(database=db, book_id=book_id)
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/books", response_model=BookResponse)
async def update_book_handler(book_data: BookUpdate, db: Session = Depends(get_db)):
    try:
        book = update_book(database=db, book_id=book_data.book_id, fields_data=book_data.fields_data)
        db.commit()
        db.refresh(book)
        return book
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/books")
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


#User---------------------------------------------------------
@app.post("/users", response_model=UserResponse)
async def create_user_handler(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(database=db, user_name=user_data.user_name, phone=user_data.phone)

        db.add(user)
        db.commit()
        return user
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users", response_model=UserResponse)
async def read_user_handler(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = find_user_by_id(database=db, user_id=user_id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/users", response_model=UserResponse)
async def update_user_handler(user_data: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = update_user(database=db, user_id=user_data.user_id, new_user_name=user_data.user_name)
        db.commit()
        db.refresh(user)
        return user
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e)


@app.delete("/users")
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
@app.post("/users_books")
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


@app.delete("/users_books")
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



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8964)
