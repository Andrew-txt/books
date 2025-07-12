import uuid
from typing import List

class Publisher:
    def __init__(self, publisher_name, country):
        self.publisher_name = publisher_name
        self.country = country
        self.publisher_id = str(uuid.uuid4())
        self.books: List["Book"] = []


    def __eq__(self, other):
        if not isinstance(other, Publisher):
            return False
        return self.publisher_name == other.publisher_name and self.country == other.country


    def __hash__(self):
        return hash((self.publisher_name, self.country))


class Author:
    def __init__(self, author_name, country):
        self.author_id = str(uuid.uuid4())
        self._author_name = author_name
        self._country = country


    @property
    def author_name(self):
        return self._author_name

    @property
    def country(self):
        return self._country


    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return self._author_name == other._author_name and self._country == other._country


    def __hash__(self):
        return hash((self._author_name, self._country))


class Book:
    def __init__(self,name, author: Author, genre, publication_year, publisher: Publisher = None):
        self._name = name
        self.book_id = str(uuid.uuid4())
        self._author = author
        self.genre = genre
        self._publication_year = publication_year
        self.publisher = publisher

        if publisher:
            publisher.books.append(self)

    @property
    def name(self):
        return self._name

    @property
    def author(self):
        return self._author

    @property
    def publication_year(self):
        return self._publication_year


    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self._author == other._author and self._name == other._name


    def __hash__(self):
        return hash((self._author, self._name))


class User:
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self.user_id = str(uuid.uuid4())
        self.favorite_books: List["Book"] = []

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._name == other._name and self._phone == other._phone

    def __hash__(self):
        return hash((self._name, self._phone))


class Storage:
    def __init__(self):
        self.publishers: List[Publisher] = []
        self.authors: List[Author] = []
        self.books: List[Book] = []
        self.users: List[User] = []