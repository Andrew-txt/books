from classes import Publisher, Author, Book, User, Storage
from bnvbhj import find_book, find_author, find_publisher, find_user
from typing import Optional


def add_publisher(storage: Storage, publisher: Publisher):
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")
    if not isinstance(publisher, Publisher):
        raise TypeError("'publisher' должен быть экземпляром класса 'Publisher'")

    if publisher in storage.publishers:
        raise ValueError("Издательство существует")

    storage.publishers.append(publisher)
    return "Издательство добавлено в хранилище"


def delete_publisher(storage: Storage, publisher_id):
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")
    if type(publisher_id) is not str:
        raise TypeError("'publisher_id' должен быть строкой")

    publisher = find_publisher(storage, publisher_id)

    if not publisher:
        raise ValueError("Издательство не найдено")

    storage.publishers.remove(publisher)
    return "Издательство удалено из хранилища"


def add_author(storage: Storage, author: Author):
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")
    if not isinstance(author, Author):
        raise TypeError("'author' должен быть экземпляром класса 'Author'")

    if author in storage.authors:
        raise ValueError("Автор существует")

    storage.authors.append(author)
    return "Автор добавлен в хранилище"


def delete_author(storage: Storage, author_id):
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")
    if type(author_id) is not str:
        raise TypeError("'author_id' должен быть строкой")

    author = find_author(storage, author_id)

    if not author:
        raise ValueError("Автор не найден")

    storage.authors.remove(author)
    return "Автор удален"


def add_book(book: Book, storage: Storage):
    if not isinstance(book, Book):
        raise TypeError("'book' должен быть экземпляром класса 'Book'")
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")

    if book in storage.books:
        raise ValueError("Книга существует")

    if book.author not in storage.authors:
        raise ValueError("Автор не найден")

    if book.publisher and book.publisher not in storage.publishers:
        raise ValueError("Издатель не найден")

    storage.books.append(book)

    if book.publisher:
        book.publisher.books.append(book)
    return "Книга добавлена"


def delete_book(book_id, storage: Storage, publisher: Optional[Publisher] = None):
    book = find_book(book_id, storage, publisher)
    if not book:
        raise ValueError("Книга не найдена")

    if book in storage.books:
        storage.books.remove(book)

    if publisher and book in publisher.books:
        publisher.books.remove(book)
    return "Книга удалена"


def add_user(user: User, storage: Storage):
    if not isinstance(user, User):
        raise TypeError("'user' должен быть экземпляром класса 'User'")
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")

    if user in storage.users:
        raise ValueError("Пользователь существует")

    storage.users.append(user)
    return "Пользователь добавлен"


def delete_user(storage: Storage, user_id):
    if not isinstance(storage, Storage):
        raise TypeError("'storage' должен быть экземпляром класса 'Storage'")
    if type(user_id) is not str:
        raise TypeError("'user_id' должен быть строкой")

    user = find_user(storage, user_id)

    if not user:
        raise ValueError("Пользователь не найден")

    storage.users.remove(user)
    return "Пользователь удален"


def add_favorite_book_to_user(book: Book, user: User):
    if not isinstance(book, Book):
        raise TypeError("'book' должен быть экземпляром класса 'Book'")
    if not isinstance(user, User):
        raise TypeError("'user' должен быть экземпляром класса 'User'")

    if book in user.favorite_books:
        raise ValueError("Книга существует")

    user.favorite_books.append(book)
    return "Книга добавлена в любимые книги пользователя"


def delete_users_favorite_book(book: Book, user: User):
    if not isinstance(book, Book):
        raise TypeError("'book' должен быть экземпляром класса 'Book'")
    if not isinstance(user, User):
        raise TypeError("'user' должен быть экземпляром класса 'User'")

    user.favorite_books.remove(book)
    return "Книга удалена из любимых книг пользователя"