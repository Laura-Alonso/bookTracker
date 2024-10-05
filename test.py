import requests
import sqlite3
from datetime import datetime

# Set up the SQLite database
def setup_database(db_name='personal.db'):
    conn = sqlite3.connect(db_name)  # Establishes a connection to the SQLite database "personal" or create it.
    cursor = conn.cursor()           # Create a cursor object used to execute SQL comands
    
    # Create a table to store book details   # Create SQL comand. Names are columns names.
    cursor.execute('''                        
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY NOT NULL,
            title TEXT,
            authors TEXT,
            description TEXT,
            published_date DATE,
            page_count TEXT,
            formato TEXT,
            language TEXT,
            genders TEXT,
            preview_link TEXT,
            image_links TEXT,
            read_date DATE,
            rate INTEGER,
            times_readed INTEGER         
        )
    ''')
    conn.commit()  # Save the changes in the database
    conn.close()   # Close the conection with the data_base


# Fetch book data from Google Books API using ISBN
def fetch_book_data_isbn(isbn):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(google_books_api_url)
    
    if response.status_code == 200:
        book_info = response.json()
        
        # Check if we have any items in the response
        if 'items' in book_info:
            book = book_info['items'][0]['volumeInfo']
            image = book.get('imageLinks', {})

            # Return a dictionary with relevant book information
            return {
                'isbn': isbn,
                'title': book.get('title', 'N/A'),
                'authors': ', '.join(book.get('authors', [])),
                'description': book.get('description', 'N/A'),
                'published_date': book.get('publishedDate', 'N/A'),
                'page_count': book.get('pageCount', 0),
                'language': book.get('language', 'N/A'),
                'genders': ', '.join(book.get('categories', [])),
                'preview_link': book.get('previewLink', 'N/A'),   
                'image_links': image.get('thumbnail', 'N/A'),              
            }
    return None

# Fetch book data from Google Books API using Title

def fetch_book_data_title(title):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(google_books_api_url)
    
    if response.status_code == 200:
        books_info = response.json()
        books = []

        # Sacar la información de los 5 primeros
        for book in books_info.get('items', [])[:5]:
            # Acceder a la información de cada libro a través de 'volumeInfo' y a traves de "industryIdentifiers"
            volume_info = book.get('volumeInfo', {})
            identifiers = volume_info.get('industryIdentifiers', [])
            image = volume_info.get('imageLinks', {})

            # Extraer la información
            isbn = next((identifier['identifier'] for identifier in identifiers if identifier['type'] == 'ISBN_13'), 'N/A')
            title = volume_info.get("title", "N/A")
            authors = ', '.join(volume_info.get('authors', []))
            description = volume_info.get('description', 'N/A')
            published_date = volume_info.get('publishedDate', 'N/A')
            page_count = volume_info.get('pageCount', 'N/A')
            language = volume_info.get('language', 'N/A')
            genders = ', '.join(volume_info.get('categories',[]))
            preview_link = volume_info.get('previewLink', 'N/A')
            image_links = image.get('thumbnail', 'N/A')

            # Agregar los detalles a la lista de libros
            books.append({
                'ISBN': isbn,
                'Title': title,
                'Author/s': authors,
                'Description': description,
                'Published date': published_date,
                'Page count': page_count,
                'Language': language,
                'Genders': genders,
                'Preview link': preview_link,
                'Image': image_links
 })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"
    

# Step 4. Insert other variables

def get_read_date():
    while True:
        read_date = input("When did you read the book for the first time? (YYYY-MM-DD or leave empty): ")
        if read_date == '':
            return None  # Permite un valor nulo si no se proporciona una fecha
        try:
            # Validar el formato de la fecha
            datetime.strptime(read_date, '%Y-%m-%d')
            return read_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format or leave empty.")

def get_rate():
    while True:
        rate = input("Rate the book (0-5 or leave empty): ")
        if rate == '':
            return None  # Permite un valor nulo si no se proporciona una fecha
        try:
            # Validar el formato de la fecha
            if rate.isdigit() and 0 <= int(rate) <= 5:
                return int(rate)
        except ValueError:
            print("Invalid rating. Please enter a number between 0 and 5 or leave empty.")

def get_times_readed():
    while True:
        times_readed = input("How many times have you read the book? (or leave empty): ")
        if times_readed == '':
            return None
        try:
            if times_readed.isdigit():
                return int(times_readed)
        except ValueError:
            print("Invalid input. Please enter a number or leave empty.")

def get_book_format():
    while True:
        print("Is the book in paper (1) or ebook (2)?")
        book_type = input("Enter 1 for paper, 2 for ebook: ")
        if book_type == '':
            return None
        elif book_type == '1':
            return 'Paper'  # Paper book
        elif book_type == '2':
            return 'Ebook'  # Ebook
        else:
            print("Invalid input. Please enter 1 for paper or 2 for ebook.")

# Show books found via API

def show_books_api(books):
    if isinstance(books, list):
        for i, books in enumerate(books, 1):
            print(f"Libro {i}:")
            print(f"  Título: {books['title']}")
            print(f"  Autor(es): {books['authors']}")
            print(f"  ISBN: {books['isbn']}")
            print(f"  Preview link: {books['preview_link']}")
            print('-' * 40)
    else:
        print(books)




# Step 3: Function to save book data to the database
def save_book_to_db(book, read_date, rate, times_readed, formato, db_name='personal.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert book data into the database
    cursor.execute('''
        INSERT OR IGNORE INTO books 
        (isbn, title, authors, description, published_date, page_count, formato, language, genders, preview_link, image_links, read_date, rate, times_readed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        book['isbn'], book['title'], book['authors'], book['description'], 
        book['published_date'],  book['page_count'], formato, book['language'], book['genders'], 
        book['preview_link'], book['image_links'], read_date, rate, times_readed
    ))
    
    conn.commit()
    conn.close()




# Step 4: Check if the book already exists in the database
def book_exists(isbn, db_name='personal.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Check if a book with the given ISBN already exists in the database
    cursor.execute('SELECT 1 FROM books WHERE isbn = ?', (isbn,))
    exists = cursor.fetchone() is not None
    
    conn.close()
    return exists


# Step 5: Ask if it want to update a exiting book
def ask_updates(isbn, db_name='personal.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Check if a book with the given ISBN already exists in the database
    cursor.execute('SELECT 1 FROM books WHERE isbn = ?', (isbn,))
    exists = cursor.fetchone() is not None
    
    conn.close()
    return exists


# Step 6: Main function to run the workflow
def main():
    setup_database()
    while True:
        isbn = input("Enter ISBN of the book (or type 'exit' to quit): ")
        if isbn.lower() == 'exit':
            break

        # Check if the book already exists
        if book_exists(isbn):
            print("The book already exists in the database.")
        else:
            
            # If book does not exist, fetch and save the book data
            books= fetch_book_data_isbn(isbn)
            if books:
                # Ask user when they read the book
                read_date = get_read_date()
                
                # Rating the book
                rate = get_rate()
                
                # Number of times readed
                times_readed = get_times_readed()
                
                # Type of book
                book_type = get_book_format()


                save_book_to_db(books, read_date, rate, times_readed, book_type)

                print(f"Book has been added to the database.")
            else:
                print("No book found with this ISBN. Please try again.")



if __name__ == "__main__":
    main()


