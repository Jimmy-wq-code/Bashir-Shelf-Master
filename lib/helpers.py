# lib/db/helper.py
from sqlalchemy.orm import joinedload
from lib.db.database import get_session
from lib.db.models import Author, Book

# ------------------------
# AUTHOR HELPERS
# ------------------------

def list_authors():
    session = get_session()
    authors = session.query(Author).all()
    session.close()
    return authors

def add_author(name, email):
    session = get_session()
    author = Author(name=name, email=email)
    session.add(author)
    session.commit()
    session.refresh(author)  # make sure instance is up-to-date
    session.close()
    return author

def find_author_by_name(name):
    session = get_session()
    author = session.query(Author).filter(Author.name.ilike(f"%{name}%")).first()
    session.close()
    return author

# ------------------------
# BOOK HELPERS
# ------------------------

def list_books():
    session = get_session()
    # Eager-load author to avoid DetachedInstanceError
    books = session.query(Book).options(joinedload(Book.author)).all()
    session.close()
    return books

def add_book(title, genre, author_id):
    session = get_session()

    author = session.get(Author, author_id)
    if not author:
        session.close()
        raise ValueError(f"❌ No author found with ID {author_id}")
    
    # Create book linked to author
    book = Book(title=title, genre=genre, author=author)
    session.add(book)
    session.commit()
    session.refresh(book)  # make sure the instance is up-to-date
    session.close()
    return book

def find_book_by_title(title):
    session = get_session()
    book = (
        session.query(Book)
        .options(joinedload(Book.author))  # load author immediately
        .filter(Book.title.ilike(f"%{title}%"))
        .first()
    )
    session.close()
    return book

def delete_book(book_id):
    session = get_session()
    book = session.get(Book, book_id)
    if book:
        session.delete(book)
        session.commit()
    session.close()
    return book
