from sqlalchemy.orm import Session
from uuid import UUID
from app.database import Publisher, Author, Book, User


def find_publisher_by_id(database: Session, publisher_id: UUID):
    publisher = database.get(Publisher, publisher_id)

    if not publisher:
        raise ValueError("Издатель не найден")
    return publisher


def find_author_by_id(database: Session, author_id: UUID):
    author = database.get(Author, author_id)

    if not author:
        raise ValueError("Автор не найден")
    return author


def find_book_by_id(database: Session, book_id: UUID):
    book = database.get(Book, book_id)

    if not book:
        raise ValueError("Книга не найдена")
    return book


def find_user_by_id(database: Session, user_id: UUID):
    user = database.get(User, user_id)

    if not user:
        raise ValueError("Пользователь не найден")
    return user