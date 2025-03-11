import streamlit as st
import json

#! File to store the library data
LIBRARY_FILE = "library.json"

#! Load the library from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

#! Save the library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)


#! Initialize library
title = "Personal Library Manager 📚"
st.set_page_config(page_title=title)
st.title(title)

if "library" not in st.session_state:
    st.session_state.library = load_library()


#! Apply custom background color
st.markdown(
    """
   <style>
        .stApp {
            background: linear-gradient(to right, #A57BC5 , #FFFFFF);
            color: black;
        }
        .stSidebar {
            background:#B89AD3;;
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
    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    st.session_state.library.append(new_book)
    save_library(st.session_state.library)
    st.sidebar.success("Book added successfully!")

#! Remove a book
st.sidebar.header("Remove a Book 🚮")
titles = [book["title"] for book in st.session_state.library]
book_to_remove = st.sidebar.selectbox("Select a book to remove", ["None"] + titles)
if st.sidebar.button("Remove Book") and book_to_remove != "None":
    st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
    save_library(st.session_state.library)
    st.sidebar.success("Book removed successfully!")

#! Search for a book
st.header("Search for a Book 🔍📕")
search_query = st.text_input("Enter a title or author to search")
if st.button("Search"):
    results = [book for book in st.session_state.library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
    if results:
        st.write("### Matching Books 📚:")
        for book in results:
            status = "Read" if book["read"] else "Unread"
            st.write(f'- **{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {status}')
    else:
        st.write("No books found ❌")

#! Display all books
st.header("All Books in Your Library 🧾")
if st.session_state.library:
    for book in st.session_state.library:
        status = "Read" if book["read"] else "Unread"
        st.write(f'- **{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {status}')
else:
    st.write("No books in your library ❌")

#! Display statistics
st.header("Library Statistics 📊")
total_books = len(st.session_state.library)
read_books = sum(1 for book in st.session_state.library if book["read"])
percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
st.write(f'**Total books:** {total_books}')
st.write(f'**Percentage read:** {percentage_read:.2f}%')
