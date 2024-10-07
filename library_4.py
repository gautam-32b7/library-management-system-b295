import psycopg2
from db_connection import create_connection
from binary_search_tree import BST

# Book class
class Book:
    def __init__(self, title, author, isbn, is_available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = is_available
    
    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}"

# Library class with database operations
class Library:
    def __init__(self):
        self.bst = BST() # Using a BST to store the books in memory
        self.load_books_from_db()
    
    # Load books from PostgreSQL into BST
    def load_books_from_db(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books_data = cursor.fetchall()

            for book_data in books_data:
                book = Book(book_data[1], book_data[2], book_data[3], book_data[4])
                self.bst.insert(book)

    # Add book
    def add_book(self, book):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO books (title, author, isbn, is_available) VALUES (%s, %s, %s, %s)", (book.title, book.author, book.isbn, book.is_available))
            conn.commit()
            self.bst.insert(book) # Add to BST
            print(f"Book '{book.title}' added successfully")
        except psycopg2.IntegrityError:
            print(f"Book with ISBN '{book.isbn}' already exists!")
        finally:
            conn.close()

    # Borrow book
    def borrow_book(self, isbn, borrower):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE isbn = %s AND is_available = True", (isbn,))
        book_data = cursor.fetchone()

        if book_data:
            cursor.execute("UPDATE books SET is_available = FALSE WHERE isbn = %s", (isbn,))
            conn.commit()
            book = self.bst.search(isbn)
            if book:
                book.is_available = False
            print(f"'{book.title}' has been borrowed by {borrower}")
        else:
            print("Book unavailable or invalid ISBN")
        conn.close()

    # Return book
    def return_bok(self, isbn):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE isbn = %s AND is_available = FALSE", (isbn,))
        book_data = cursor.fetchone()

        if book_data:
            cursor.execute("UPDATE books SET is_available = TRUE WHERE isbn = %s", (isbn,))
            conn.commit()
            book = self.bst.search(isbn)
            if book:
                book.is_available = True
            print(f"'{book.title}' has been returned!")
        else:
            print("Invalid ISBN or the book is already available")
        conn.close()

    # Display available book
    def display_available_books(self):
        available_books = [book for book in self.bst.inorder_traversal() if book.is_available]
        if available_books:
            print("\nAvailable Books: ")
            for book in available_books:
                print(book)
        else:
            print("No books available")
    
    # Display borrowed books
    def display_borrowed_books(self):
        borrowed_books = [book for book in self.bst.inorder_traversal() if not book.is_available]
        if borrowed_books:
            print("\nBorrowed Books: ")
            for book in borrowed_books:
                print(book)
        else:
            print("No books are currently borrowed")

# Main application logic
def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View Available Books")
        print("5. View Borrowed Books")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            book = Book(title, author, isbn)
            library.add_book(book)
        elif choice == '2':
            isbn = input("Enter ISBN of the book to borrow: ")
            borrower = input("Enter your name: ")
            library.borrow_book(isbn, borrower)
        elif choice == '3':
            isbn = input("Enter ISBN of the book to return: ")
            library.return_bok(isbn)
        elif choice == '4':
            library.display_available_books()
        elif choice == '5':
            library.display_borrowed_books()
        elif choice == '6':
            print("Exiting the Library Management System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()