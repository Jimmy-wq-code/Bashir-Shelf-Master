# lib/db/helpers.py
from sqlalchemy.orm import joinedload
from lib.db.database import get_session
from lib.db.models import Author, Book, Member, BorrowRecord
from datetime import datetime

# AUTHOR HELPERS
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
    session.refresh(author)
    session.close()
    return author

def find_author_by_name(name):
    session = get_session()
    author = session.query(Author).filter(Author.name.ilike(f"%{name}%")).first()
    session.close()
    return author

# BOOK HELPERS
def list_books():
    session = get_session()
    books = session.query(Book).options(joinedload(Book.author)).all()
    
    # Handle books with missing author
    for book in books:
        if book.author is None:
            book.author = type('Author', (), {'name': 'Unknown'})()
    
    session.close()
    return books

def add_book(title, genre, author_id):
    session = get_session()
    author = session.get(Author, author_id)
    if not author:
        session.close()
        raise ValueError("Author ID does not exist")
    
    book = Book(title=title, genre=genre, author_id=author_id)
    session.add(book)
    session.commit()
    session.refresh(book)
    session.close()
    return book

def find_book_by_title(title):
    session = get_session()
    book = (
        session.query(Book)
        .options(joinedload(Book.author))
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

# MEMBER HELPERS
def register_member(name, email):
    session = get_session()
    # Check if email already exists
    if session.query(Member).filter_by(email=email).first():
        session.close()
        raise ValueError("Email already registered")
    
    member = Member(name=name, email=email)
    session.add(member)
    session.commit()
    session.refresh(member)
    session.close()
    return member

def list_members():
    session = get_session()
    members = session.query(Member).all()
    session.close()
    return members

def borrow_book(member_id, book_id):
    session = get_session()
    member = session.get(Member, member_id)
    book = session.get(Book, book_id)

    if not member:
        session.close()
        raise ValueError("Member does not exist")
    if not book:
        session.close()
        raise ValueError("Book does not exist")
    if book.status != "available":
        session.close()
        raise ValueError("Book is currently borrowed")

    record = BorrowRecord(book=book, member=member, borrow_date=datetime.utcnow())
    book.status = "borrowed"
    session.add(record)
    session.commit()

    record = session.query(BorrowRecord)\
        .options(joinedload(BorrowRecord.book), joinedload(BorrowRecord.member))\
        .get(record.id)
    

    result = {
        "record_id": record.id,
        "book_title": record.book.title,
        "member_name": record.member.name
    }

    session.close()
    return result


def return_book(member_id, book_id):
    session = get_session()
    record = (
        session.query(BorrowRecord)
        .options(joinedload(BorrowRecord.book))
        .filter_by(member_id=member_id, book_id=book_id, return_date=None)
        .first()
    )

    if not record:
        session.close()
        raise ValueError("No active borrow record found for this member and book")

    record.return_date = datetime.utcnow()
    record.book.status = "available"
    session.commit()

   
    result = {
        "record_id": record.id,
        "book_title": record.book.title
    }

    session.close()
    return result
