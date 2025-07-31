from sqlalchemy import inspect, and_
from sqlalchemy.orm import Session

from .database import Publisher, Author, Book, User, UserFavoriteBook
from .models import *

from .utils import (
    find_author_by_id,
    find_publisher_by_id,
    find_book_by_id,
    find_user_by_id,
)


#Publisher--------------------------------------------------------
def create_publisher(database: Session, publisher_name: str, country: str):
    publisher_exists = database.query(Publisher).filter(
        Publisher.publisher_name.ilike(publisher_name),
        Publisher.country.ilike(country)
    ).first()

    if publisher_exists:
        raise ValueError("Publisher already exists")

    return Publisher(publisher_name=publisher_name,country=country)


def update_publisher(database: Session, publisher_id: UUID, fields_data: dict[str, Any]):
    publisher = find_publisher_by_id(database, publisher_id)
    changeable_fields = {"publisher_name", "country"}

    for key, value in fields_data.items():
        if key in changeable_fields:
                setattr(publisher, key, value)
        else:
            raise ValueError("Unknown field")

    return publisher


#Author--------------------------------------------------------
def create_author(database: Session, author_name:str, country: str):
    author_exists = database.query(Author).filter(
        Author.author_name.ilike(author_name),
        Author.country.ilike(country)
    ).first()

    if author_exists:
        raise ValueError("Author already exists")

    return Author(author_name=author_name, country=country)


def update_author(database: Session, author_id: UUID, fields_data: dict[str, Any]):
    author = find_author_by_id(database, author_id)
    changeable_fields = {"author_name", "country"}

    for key, value in fields_data.items():
        if key in changeable_fields:
                setattr(author, key, value)
        else:
            raise ValueError("Unknown field")

    return author


#Book--------------------------------------------------------
def create_book(
        database: Session,
        book_name: str,
        genre: str,
        publication_year: int,
        author_id: UUID,
        publisher_id: Optional[UUID] = None):
    book_exists = database.query(Book).filter(
        and_(
            Book.book_name.ilike(book_name),
            Book.author_id == author_id,
            Book.publisher_id == publisher_id
        )
    ).first()

    if book_exists:
        raise ValueError("Книга уже существует")

    author = database.query(Author).filter_by(author_id=author_id).first()

    if not author:
        raise ValueError("Неизвестный автор")

    return Book(
        book_name=book_name,
        genre=genre,
        publication_year=publication_year,
        author_id=author_id,
        publisher_id=publisher_id
    )


def update_book(database: Session, book_id: UUID, fields_data: dict[str, Any]):
    book = find_book_by_id(database, book_id)
    changeable_fields = {"book_name", "genre"}

    for key, value in fields_data.items():
        if key in changeable_fields:
                setattr(book, key, value)
        else:
            raise ValueError("Unknown field")

    return book


#User--------------------------------------------------------
def create_user(database: Session, user_name: str, phone: str):
    user_exists = database.query(User).filter(
        inspect(User.user_name == user_name),
        inspect(User.phone == phone)
    ).first()

    if user_exists:
        raise ValueError("User already exists")                        #ttttt

    return User(user_name=user_name, phone=phone)


def update_user(database: Session, user_id: UUID, new_user_name: str):
    user = find_user_by_id(database, user_id)
    user.user_name = new_user_name
    return user


#Favorite_books--------------------------------------------------------
def add_favorite_book_to_user(database: Session, user_id: UUID, book_id: UUID):
    if database.query(UserFavoriteBook).filter_by(user_id=user_id, book_id=book_id).first():
        raise ValueError("Book is already in list of favorites books")              #ttttttt

    return UserFavoriteBook(user_id=user_id, book_id=book_id)