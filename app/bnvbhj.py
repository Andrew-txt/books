from classes import Publisher, Storage
from typing import Optional


def find_user(storage: Storage, user_id):
    for user in storage.users:
        if user.user_id == user_id:
            return user


def find_publisher(storage: Storage, publisher_id):
    for publisher in storage.publishers:
        if publisher.publisher_id == publisher_id:
            return publisher


def find_author(storage: Storage, author_id):
    for author in storage.authors:
        if author.author_id == author_id:
            return author


def find_book(book_id, storage: Storage, publisher: Optional[Publisher] = None):
    if publisher:
        for book in publisher.books:
            if book.book_id == book_id:
                return book

    for book in storage.books:
        if book.book_id == book_id:
            return book

    return None