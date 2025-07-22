from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()
URL = "postgresql://diana1215:314159265@localhost:5432/Books"
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

class Publisher(Base):
    __tablename__ = "publishers"
    publisher_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, immutable=True)
    publisher_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.publisher_id}, name='{self.publisher_name}', country='{self.country}')>"

class Author(Base):
    __tablename__ = "authors"
    author_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, immutable=True)
    author_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Author(id={self.author_id}, name='{self.author_name}', country='{self.country}'>"

class Book(Base):
    __tablename__ = "books"
    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, immutable=True)
    book_name = Column(String(100), nullable=False)
    genre = Column(String(100), nullable=False)
    publication_year = Column(Integer, immutable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.author_id"))
    publisher_id = Column(UUID(as_uuid=True), ForeignKey("publishers.publisher_id"))
    author = relationship("Author")
    publisher = relationship("Publisher", back_populates="books")

    def __repr__(self):
        return f"<Book(id='{self.book_id}', name='{self.book_name}', publisher_id='{self.publisher_id}', author_id='{self.author_id}'>"

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, immutable=True)
    user_name = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True, immutable=True)
    favorite_books = relationship("UserFavoriteBook", back_populates="user")

    def __repr__(self):
        return f"<User(id='{self.user_id}', name='{self.user_name}'>"

class UserFavoriteBook(Base):
    __tablename__ = "user_favorite_books"
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True, immutable=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.book_id'), primary_key=True, immutable=True)
    user = relationship("User", back_populates="favorite_books")
    book = relationship("Book")

Base.metadata.create_all(bind=engine)