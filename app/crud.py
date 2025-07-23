# здесь будут crud методы (c - str, r - obj, u - obj, d - str)
from uuid import UUID
from typing import Any, Optional

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from database import Publisher, Author, Book, User, UserFavoriteBook

from app.utils import (
    find_author_by_id,
    find_publisher_by_id,
    find_book_by_id,
    find_user_by_id,
    type_assert
)


#Publisher--------------------------------------------------------
@type_assert(Session, str, str)
def create_publisher(database: Session, publisher_name: str, country: str):
    publisher_exists = database.query(Publisher).filter(
        Publisher.publisher_name.ilike(publisher_name),
        Publisher.country.ilike(country)
    ).first()

    if publisher_exists:
        raise ValueError("Издательство уже существует")

    publisher = Publisher(publisher_name=publisher_name,country=country)

    database.add(publisher)
    database.commit()
    database.refresh(publisher)
    return publisher


@type_assert(Session, UUID)
def read_publisher(database: Session, publisher_id: UUID):
    publisher = find_publisher_by_id(database, publisher_id)
    return publisher


@type_assert(Session, UUID, dict)
def update_publisher(database: Session, publisher_id: UUID, fields_data: dict[str, Any]):
    publisher = find_publisher_by_id(database, publisher_id)
    changeable_fields = {"publisher_name", "country"}

    for key, value in fields_data.items():
        if key in changeable_fields:
            if hasattr(publisher, key):
                setattr(publisher, key, value)
        else:
            raise ValueError("Неизвестное поле")

    database.commit()
    database.refresh(publisher)
    return publisher


@type_assert(Session, UUID)
def delete_publisher(database: Session, publisher_id: UUID):
    publisher = database.query(Publisher).filter_by(publisher_id=publisher_id).first()

    if not publisher:
        raise ValueError("Издатель не найден")

    database.delete(publisher)
    database.commit()
    return "Издатель удален"


#Author--------------------------------------------------------
@type_assert(Session, str, str)
def create_author(database: Session, author_name:str, country: str):
    author_exists = database.query(Author).filter(
        Author.author_name.ilike(author_name),
        Author.country.ilike(country)
    ).first()

    if author_exists:
        raise ValueError("Автор уже существует")

    author = Author(author_name=author_name, country=country)

    database.add(author)
    database.commit()
    return "Автор создан"


@type_assert(Session, UUID)
def read_author(database:Session, author_id: UUID):
    author = find_author_by_id(database, author_id)
    return author


@type_assert(Session, UUID, dict)
def update_author(database: Session, author_id: UUID, fields_data: dict[str, Any]):
    author = find_author_by_id(database, author_id)
    changeable_fields = {"author_name", "country"}

    for key, value in fields_data.items():
        if key in changeable_fields:
            if hasattr(author, key):
                setattr(author, key, value)
        else:
            raise ValueError("Неизвестное поле")

    database.commit()
    database.refresh(author)
    return author


@type_assert(Session, UUID)
def delete_author(database: Session, author_id: UUID):
    author = find_author_by_id(database, author_id)

    database.delete(author)
    database.commit()
    return "Автор удален"


#Book--------------------------------------------------------
@type_assert(Session, str, str, int, UUID, Optional[UUID])
def create_book(
        database: Session,
        book_name: str,
        genre: str,                             # добавить pydantic модель в будущем
        publication_year: int,
        author_id: UUID,
        publisher_id: Optional[UUID] = None):
    book_exists = database.query(Book).filter(
        Book.book_name.ilike(book_name),
        Book.author_id.ilike(author_id),
        Book.publisher_id.ilike(publisher_id)
    ).first()
    if book_exists:
        raise ValueError("Книга уже существует")

    author = database.query(Author).filter_by(author_id=author_id).first()
    if not author:
        raise ValueError("Неизвестный автор")

    book = Book(
        book_name=book_name,
        genre=genre,
        publication_year=publication_year,
        author_id=author_id,
        publisher_id=publisher_id
    )

    if publisher_id:
        publisher = database.get(Publisher, publisher_id)
        if publisher:
            publisher.books.append(book)

    database.add(book)
    database.commit()
    return "Книга создана"


@type_assert(Session, UUID)
def read_book(database: Session, book_id: UUID):
    book = find_book_by_id(database, book_id)
    return book


@type_assert(Session, UUID, dict)
def update_book(database: Session, book_id: UUID, fields_data: dict[str, Any]):
    book = find_book_by_id(database, book_id)
    changeable_fields = {"book_name", "genre"}

    for key, value in fields_data.items():
        if key in changeable_fields:
            if hasattr(book, key):
                setattr(book, key, value)
        else:
            raise ValueError("Неизвестное поле")

    database.commit()
    database.refresh(book)
    return book


@type_assert(Session, UUID, Optional[UUID])
def delete_book(database: Session, book_id: UUID, publisher_id: Optional[UUID] = None):
    book = find_book_by_id(database, book_id)

    if publisher_id is not None:
        publisher = find_publisher_by_id(database, publisher_id)
    else:
        publisher = None

    if publisher:
        publisher.books.remove(book)

    database.delete(book)
    database.commit()
    return "Книга удалена"


#User--------------------------------------------------------
@type_assert(Session, str, str)
def create_user(database: Session, user_name: str, phone: str):
    user_exists = database.query(User).filter(
        inspect(User.user_name == user_name),
        inspect(User.phone == phone)
    ).first()

    if user_exists:
        raise ValueError("Пользователь с такими же данными уже существует")

    user = User(user_name=user_name, phone=phone)

    database.add(user)
    database.commit()
    return "Пользователь создан"


@type_assert(Session, UUID)
def read_user(database: Session, user_id: UUID):
    user = find_user_by_id(database, user_id)
    return user


@type_assert(Session, UUID, str)
def update_user(database: Session, user_id: UUID, new_user_name: str):
    user = find_user_by_id(database, user_id)
    user.user_name = new_user_name

    database.commit()
    database.refresh(user)
    return user


@type_assert(Session, UUID)
def delete_user(database: Session, user_id: UUID):
    user = find_user_by_id(database, user_id)
    database.query(UserFavoriteBook).filter_by(user_id=user_id).delete()

    database.delete(user)
    database.commit()
    return "Пользователь удален"


#Favorite_books--------------------------------------------------------
@type_assert(Session, UUID, UUID)
def add_favorite_book_to_user(database: Session, user_id: UUID, book_id: UUID):
    if database.query(UserFavoriteBook).filter_by(user_id=user_id, book_id=book_id).first():
        return "Книга уже в любимом"

    favorite_book = UserFavoriteBook(user_id=user_id, book_id=book_id)
    database.add(favorite_book)
    database.commit()
    return "Книга добавлена в список любимых книг пользователя"


@type_assert(Session, UUID, UUID)
def delete_users_favorite_book(database: Session, user_id: UUID, book_id: UUID):
    book = database.query(UserFavoriteBook). filter_by(user_id=user_id, book_id=book_id).first()

    if not book:
        raise ValueError("Книга не найдена")

    database.delete(book)
    database.commit()
    return "Книга удалена из списка любимых книг пользователя"
