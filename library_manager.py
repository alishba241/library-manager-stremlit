import streamlit as st
from database import add_book, remove_book, search_books, get_all_books, get_book_counts

st.set_page_config(page_title="Personal Library Manager 📚")
st.title("Personal Library Manager 📚")

#! Apply custom background color
st.markdown(
    """
   <style>
        .stApp {
            background: linear-gradient(to right, #A57BC5 , #FFFFFF);
            color: black;
        }
        .stSidebar {
            background:rgba(255, 255, 255, 0.2);
            color: white;
        }
        .stButton>button {
            background-color: black;
            color: white;

            }
            
    </style>
    """,
    unsafe_allow_html=True
)

#! Add a book
st.sidebar.header("Add a New Book 📕")
title = st.sidebar.text_input("Title")
author = st.sidebar.text_input("Author")
year = st.sidebar.number_input("Publication Year", min_value=0, step=1)
genre = st.sidebar.text_input("Genre")
read_status = st.sidebar.checkbox("Have you read this book?")

if st.sidebar.button("Add Book"):
    add_book(title, author, year, genre, read_status)
    st.sidebar.success("Book added successfully!")

#! Remove a book
st.sidebar.header("Remove a Book 🚮")
books = get_all_books()
titles = [book[0] for book in books]  # Extracting titles from the list of books
book_to_remove = st.sidebar.selectbox("Select a book to remove", ["None"] + titles)

if st.sidebar.button("Remove Book") and book_to_remove != "None":
    remove_book(book_to_remove)
    st.sidebar.success("Book removed successfully!")

#! Search for a book
st.header("Search for a Book 🔍📕")
search_query = st.text_input("Enter a title or author to search")

if st.button("Search"):
    results = search_books(search_query)
    if results:
        st.header("Matching Books 📚:")
        for book in results:
            status = "Read" if book[4] else "Unread"
            st.write(f'- **{book[0]}** by {book[1]} ({book[2]}) - {book[3]} - {status}')
    else:
        st.write("No books found ❌")

#! Display all books
st.header("All Books in Your Library 🧾")
all_books = get_all_books()
if all_books:
    for book in all_books:
        status = "Read" if book[4] else "Unread"
        st.write(f'- **{book[0]}** by {book[1]} ({book[2]}) - {book[3]} - {status}')
else:
    st.write("No books in your library ❌")

#! Display statistics
st.header("Library Statistics 📊")

#! fetching book count from database
total_books, read_books = get_book_counts()
percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

st.write(f'**Total books:** {total_books}')
st.write(f'**Percentage read:** {percentage_read:.2f}%')

