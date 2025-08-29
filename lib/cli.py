# lib/cli.py
import sys, os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.helpers import (
    list_authors, add_author, find_author_by_name,
    list_books, add_book, find_book_by_title, delete_book,
    register_member, borrow_book, return_book, list_members
)

def main_menu():
    while True:
        print("\n📚 Welcome to Bashir-Shelf-Master 📚")
        print("1. Manage Authors")
        print("2. Manage Books")
        print("3. Manage Members")
        print("4. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            author_menu()
        elif choice == "2":
            book_menu()
        elif choice == "3":
            member_menu()
        elif choice == "4":
            print("👋 Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Try again.")

# AUTHOR MENU
def author_menu():
    while True:
        print("\n👤 Author Menu")
        print("1. List all authors")
        print("2. Add new author")
        print("3. Search author by name")
        print("4. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            authors = list_authors()
            if authors:
                for a in authors:
                    print(f"- {a.id}: {a.name} ({a.email})")
            else:
                print("No authors found.")
        elif choice == "2":
            name = input("Enter author name: ")
            email = input("Enter author email: ")
            add_author(name, email)
            print("✅ Author added!")
        elif choice == "3":
            name = input("Enter name to search: ")
            author = find_author_by_name(name)
            if author:
                print(f"Found: {author.id} - {author.name} ({author.email})")
            else:
                print("❌ Author not found.")
        elif choice == "4":
            return
        else:
            print("❌ Invalid choice. Try again.")

# BOOK MENU
def book_menu():
    while True:
        print("\n📖 Book Menu")
        print("1. List all books")
        print("2. Add new book")
        print("3. Search book by title")
        print("4. Delete a book")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            books = list_books()
            if books:
                for b in books:
                    author_name = b.author.name if b.author else "Unknown"
                    print(f"- {b.id}: {b.title} ({b.genre}) by {author_name}")
            else:
                print("No books found.")
        elif choice == "2":
            title = input("Enter book title: ")
            genre = input("Enter genre: ")
            author_id = input("Enter author ID: ")
            try:
                author_id = int(author_id)
                add_book(title, genre, author_id)
                print("✅ Book added!")
            except ValueError as e:
                print(f"❌ Error: {e}")
        elif choice == "3":
            title = input("Enter title to search: ")
            book = find_book_by_title(title)
            if book:
                author_name = book.author.name if book.author else "Unknown"
                print(f"Found: {book.id} - {book.title} ({book.genre}) by {author_name}")
            else:
                print("❌ Book not found.")
        elif choice == "4":
            book_id = input("Enter book ID to delete: ")
            try:
                book_id = int(book_id)
                deleted = delete_book(book_id)
                if deleted:
                    print("✅ Book deleted!")
                else:
                    print("❌ Book not found.")
            except ValueError:
                print("❌ Invalid book ID.")
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice. Try again.")

# MEMBER MENU
def member_menu():
    while True:
        print("\n👥 Member Menu")
        print("1. Register as member")
        print("2. List all members")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            try:
                member = register_member(name, email)
                print(f"✅ Member registered: {member.name}")
            except ValueError as e:
                print(f"❌ {e}")

        elif choice == "2":
            members = list_members()
            for m in members:
                print(f"- {m.id}: {m.name} ({m.email})")

        elif choice == "3":
            member_id = int(input("Enter your member ID: "))
            book_id = int(input("Enter book ID to borrow: "))
            try:
                record = borrow_book(member_id, book_id)
                print(f"✅ You borrowed: {record['book_title']}")
            except ValueError as e:
                print(f"❌ {e}")

        elif choice == "4":
            member_id = int(input("Enter your member ID: "))
            book_id = int(input("Enter book ID to return: "))
            try:
                record = return_book(member_id, book_id)
                print(f"✅ You returned: {record['book_title']}")
            except ValueError as e:
                print(f"❌ {e}")

        elif choice == "5":
            return
        else:
            print("❌ Invalid choice. Try again.")



if __name__ == "__main__":
    main_menu()
