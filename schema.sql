CREATE TABLE IF NOT EXISTS publishers (
    publisher_id UUID PRIMARY KEY,
    publisher_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
    author_id UUID PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    book_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    publication_year INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL UNIQUE
    phone VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user_favorite_books (
    user_id UUID REFERENCES users(user_id),
    book_id UUID REFERENCES books(book_id),
    PRIMARY KEY (user_id, book_id)
);