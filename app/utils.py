from sqlalchemy.orm import Session
from app.database import Publisher, Author, Book, User
from typing import get_origin, get_args, Union
from uuid import UUID
import inspect
from functools import wraps


def find_publisher_by_id(database: Session, publisher_id: UUID):
    publisher = database.get(Publisher, publisher_id)

    if not publisher:
        raise ValueError("Publisher not found")
    return publisher


def find_author_by_id(database: Session, author_id: UUID):
    author = database.get(Author, author_id)

    if not author:
        raise ValueError("Author not found")
    return author


def find_book_by_id(database: Session, book_id: UUID):
    book = database.get(Book, book_id)

    if not book:
        raise ValueError("Book not found")
    return book


def find_user_by_id(database: Session, user_id: UUID):
    user = database.get(User, user_id)

    if not user:
        raise ValueError("User not found")
    return user


def type_assert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name not in bound_types:
                    continue
                expected_type = bound_types[name]
                if value is None and get_origin(expected_type) is Union:
                    continue
                if (expected_type is UUID or
                        (get_origin(expected_type) is Union and UUID in get_args(expected_type))):
                    if isinstance(value, str):
                        try:
                            bound_values.arguments[name] = UUID(value)
                        except ValueError:
                            raise TypeError(f'Argument {name} is not a valid UUID string')
                    elif not isinstance(value, UUID):
                        raise TypeError(f'Argument {name} must be UUID or str')
                elif get_origin(expected_type) is None and not isinstance(value, expected_type):
                    raise TypeError(f'Argument {name} must be {expected_type}')
            return func(*bound_values.args, **bound_values.kwargs)
        return wrapper
    return decorate


