import uuid

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, validates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import inspect

from config import DB_CONFIG


Base = declarative_base()
engine = create_engine(DB_CONFIG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def validate_immutable_field(model, key, value):
    inspector = inspect(model)
    if key in inspector.mapper.attrs and getattr(model, key) != value:
        raise ValueError(f"Field {key} cannot be changed")
    return value


class Publisher(Base):
    __tablename__ = "publishers"
    publisher_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publisher_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.publisher_id}, name='{self.publisher_name}', country='{self.country}')>"

    @validates("publisher_id")
    def validate_publisher_id(self, key, value):
        return validate_immutable_field(self, key, value)

class Author(Base):
    __tablename__ = "authors"
    author_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Author(id={self.author_id}, name='{self.author_name}', country='{self.country}'>"

    @validates("author_id")
    def validate_author_id(self, key, value):
        return validate_immutable_field(self, key, value)

class Book(Base):
    __tablename__ = "books"
    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_name = Column(String(100), nullable=False)
    genre = Column(String(100), nullable=False)
    publication_year = Column(Integer)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.author_id"))
    publisher_id = Column(UUID(as_uuid=True), ForeignKey("publishers.publisher_id"))
    author = relationship("Author")
    publisher = relationship("Publisher", back_populates="books")

    def __repr__(self):
        return f"<Book(id='{self.book_id}', name='{self.book_name}', publisher_id='{self.publisher_id}', author_id='{self.author_id}'>"

    @validates("book_id")
    def validate_book_id(self, key, value):
        return validate_immutable_field(self, key, value)

    @validates("publication_year")
    def validate_publication_year(self, key, value):
        return validate_immutable_field(self, key, value)
                                                                            # потом добавить норм неизменяемость, а не это дерьмище
    @validates("author_id")
    def validate_author_id(self, key, value):
        return validate_immutable_field(self, key, value)

    @validates("publisher_id")
    def validate_publisher_id(self, key, value):
        return validate_immutable_field(self, key, value)


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    favorite_books = relationship("UserFavoriteBook", back_populates="user")

    def __repr__(self):
        return f"<User(id='{self.user_id}', name='{self.user_name}'>"

    @validates("user_id")
    def validate_user_id(self, key, value):
        return validate_immutable_field(self, key, value)

    @validates("phone")
    def validate_phone(self, key, value):
        return validate_immutable_field(self, key, value)


class UserFavoriteBook(Base):
    __tablename__ = "user_favorite_books"
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.book_id'), primary_key=True)
    user = relationship("User", back_populates="favorite_books")
    book = relationship("Book")

    @validates("user_id")
    def validate_user_id(self, key, value):
        return validate_immutable_field(self, key, value)

    @validates("book_id")
    def validate_book_id(self, key, value):
        return validate_immutable_field(self, key, value)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)