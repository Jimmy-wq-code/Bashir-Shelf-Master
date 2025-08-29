# lib/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from lib.db.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(name='{self.name}')>"

    # ORM methods
    @classmethod
    def create(cls, session: Session, **kwargs):
        author = cls(**kwargs)
        session.add(author)
        session.commit()
        return author

    @classmethod
    def delete(cls, session: Session, id):
        author = session.get(cls, id)
        if author:
            session.delete(author)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, id):
        return session.get(cls, id)

    @classmethod
    def find_by_attribute(cls, session: Session, attr_name: str, value):
        if not hasattr(cls, attr_name):
            raise ValueError(f"{cls.__name__} has no attribute '{attr_name}'")
        return session.query(cls).filter(getattr(cls, attr_name) == value).all()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    status = Column(String, default="available")

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book")

    def __repr__(self):
        return f"<Book(title='{self.title}', genre='{self.genre}', status='{self.status}')>"

    @classmethod
    def create(cls, session: Session, **kwargs):
        book = cls(**kwargs)
        session.add(book)
        session.commit()
        return book

    @classmethod
    def delete(cls, session: Session, id):
        book = session.get(cls, id)
        if book:
            session.delete(book)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, id):
        return session.get(cls, id)

    @classmethod
    def find_by_attribute(cls, session: Session, attr_name: str, value):
        if not hasattr(cls, attr_name):
            raise ValueError(f"{cls.__name__} has no attribute '{attr_name}'")
        return session.query(cls).filter(getattr(cls, attr_name) == value).all()


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)

    borrow_records = relationship("BorrowRecord", back_populates="member")

    def __repr__(self):
        return f"<Member(name='{self.name}', email='{self.email}')>"

    @classmethod
    def create(cls, session: Session, **kwargs):
        member = cls(**kwargs)
        session.add(member)
        session.commit()
        return member

    @classmethod
    def delete(cls, session: Session, id):
        member = session.get(cls, id)
        if member:
            session.delete(member)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, id):
        return session.get(cls, id)

    @classmethod
    def find_by_attribute(cls, session: Session, attr_name: str, value):
        if not hasattr(cls, attr_name):
            raise ValueError(f"{cls.__name__} has no attribute '{attr_name}'")
        return session.query(cls).filter(getattr(cls, attr_name) == value).all()


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))

    book = relationship("Book", back_populates="borrow_records")
    member = relationship("Member", back_populates="borrow_records")

    def __repr__(self):
        returned = self.return_date is not None
        return f"<BorrowRecord(book_id={self.book_id}, member_id={self.member_id}, returned={returned})>"

    @classmethod
    def create(cls, session: Session, **kwargs):
        record = cls(**kwargs)
        session.add(record)
        session.commit()
        return record

    @classmethod
    def delete(cls, session: Session, id):
        record = session.get(cls, id)
        if record:
            session.delete(record)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session: Session, id):
        return session.get(cls, id)

    @classmethod
    def find_by_attribute(cls, session: Session, attr_name: str, value):
        if not hasattr(cls, attr_name):
            raise ValueError(f"{cls.__name__} has no attribute '{attr_name}'")
        return session.query(cls).filter(getattr(cls, attr_name) == value).all()
