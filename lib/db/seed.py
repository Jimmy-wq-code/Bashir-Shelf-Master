# lib/db/seed.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from lib.db.database import engine, Base, SessionLocal
from lib.db.models import Author, Book, Member, BorrowRecord
from datetime import datetime

# --- Reset Database ---
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# --- Authors ---
author1 = Author(name="Jimmy Okwiri", email="jimmy.okwiri@example.com")
author2 = Author(name="J.K. Rowling", email="jkrowling@example.com")
author3 = Author(name="Tenisha Ann", email="tenishaann12@example.com")
author4 = Author(name="Sian Njoki", email="sian.njoki@example.com")
author5 = Author(name="Ann Wairimu", email="annwairimu69@example.com")

session.add_all([author1, author2, author3, author4, author5])
session.commit()

# --- Books ---
book1 = Book(title="1984", genre="Dystopian", status="available", author=author1)
book2 = Book(title="Animal Farm", genre="Political Satire", status="available", author=author1)
book3 = Book(title="Harry Potter and the Sorcerer's Stone", genre="Fantasy", status="available", author=author2)
book4 = Book(title="Things Fall Apart", genre="Historical Fiction", status="available", author=author3)
book5 = Book(title="To Kill a Mockingbird", genre="Classic", status="available", author=author4)
book6 = Book(title="Pride and Prejudice", genre="Romance", status="available", author=author4)
book7 = Book(title="The Great Gatsby", genre="Classic", status="available", author=author2)  
book8 = Book(title="The Hobbit", genre="Fantasy", status="available", author=author3)
book9 = Book(title="Crime and Punishment", genre="Philosophical Fiction", status="available", author=author5)

session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9])
session.commit()

# --- Members ---
member1 = Member(name="Alice Johnson", email="alice@example.com")
member2 = Member(name="Bob Smith", email="bob@example.com")

session.add_all([member1, member2])
session.commit()

# --- Borrow Records ---
borrow1 = BorrowRecord(book=book1, member=member1, borrow_date=datetime(2025, 8, 1))
borrow2 = BorrowRecord(book=book3, member=member2, borrow_date=datetime(2025, 8, 15))

session.add_all([borrow1, borrow2])
session.commit()

print("✅ Database seeded successfully!")

session.close()
