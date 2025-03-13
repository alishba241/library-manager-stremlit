import sqlite3

#! sqLite database file
DB_FILE = "library.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER,
                        genre TEXT,
                        read_status INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

#! database connection
def get_connection():
    return sqlite3.connect(DB_FILE)

#! initialize the database (create table if not exists)

create_table()

#! CRUD operations

#! function to add a new book
def add_book(title, author, year, genre, read_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)", 
                   (title, author, year, genre, int(read_status)))
    conn.commit()
    conn.close()

#! function to remove a book
def remove_book(title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

#! function to search a  book
def search_books(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, year, genre, read_status FROM books WHERE title LIKE ? OR author LIKE ?", 
                   (f'%{query}%', f'%{query}%'))
    books = cursor.fetchall()
    conn.close()
    return books

#! function to check book read status
def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, year, genre, read_status FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

#! function to get book counts
def get_book_counts():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    #! total books count
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    #! read books count
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]

    conn.close()
    return total_books, read_books

