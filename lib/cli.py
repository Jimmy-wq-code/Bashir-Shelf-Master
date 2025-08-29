# lib/cli.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.helpers import (
    list_authors, add_author, find_author_by_name,
    list_books, add_book, find_book_by_title, delete_book
)

def main_menu():
    while True:
        print("\n📚 Welcome to Bashir-Shelf-Master 📚")
        print("1. Manage Authors")
        print("2. Manage Books")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            author_menu()
        elif choice == "2":
            book_menu()
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Try again.")


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
            except ValueError:
                print("❌ Invalid author ID.")

        elif choice == "3":
            title = input("Enter title to search: ")
            book = find_book_by_title(title)
            if book:
                print(f"Found: {book.id} - {book.title} ({book.genre}) by {book.author.name}")
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


if __name__ == "__main__":
    main_menu()
