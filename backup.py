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
            isbn TEXT PRIMARY KEY,
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


# Obtener datos de los libro
def fetch_book_data(api_url, limit=None):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        books_info = response.json()
        books = []

        # Obtener los libros (todos o con límite)
        items = books_info.get('items', [])
        if limit is not None:
            items = items[:limit]

        # Acceder a la información de cada libro
        for book in items:
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
            genders = ', '.join(volume_info.get('categories', []))
            preview_link = volume_info.get('previewLink', 'N/A')
            image_links = image.get('thumbnail', 'N/A')

            # Agregar los detalles a la lista de libros
            books.append({
                'isbn': isbn,
                'title': title,
                'authors': authors,
                'description': description,
                'published_date': published_date,
                'page_count': page_count,
                'language': language,
                'genders': genders,
                'preview_link': preview_link,
                'image_links': image_links
            })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"


# Fetch book data from Google Books API using ISBN

def fetch_book_data_isbn(isbn):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    return fetch_book_data(google_books_api_url, limit=1)
    

# Fetch book data from Google Books API using Title

def fetch_book_data_title(title):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    return fetch_book_data(google_books_api_url, limit=5)

# Fetch book data from Google Books API using Author

def fetch_book_data_author(author):

    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    books = fetch_book_data(google_books_api_url, limit=30)
    libros_filtrados = [book for book in books if author in book.get('authors', '')]
    
    return libros_filtrados


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
def save_book_to_db(book, read_date, rate, times_readed, formate, db_name='personal.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("Book succesfully added")
    
    # Insert book data into the database
    cursor.execute('''
        INSERT OR IGNORE INTO books 
        (isbn, title, authors, description, published_date, page_count, formato, language, genders, preview_link, image_links, read_date, rate, times_readed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        book['isbn'], book['title'], book['authors'], book['description'], 
        book['published_date'],  book['page_count'], formate, book['language'], book['genders'], 
        book['preview_link'], book['image_links'], read_date, rate, times_readed
    ))
    
    conn.commit()
    conn.close()




def show_authors(books):
    if isinstance(books, list):
        for i, book in enumerate(books, 1):
            print(f"Autor {i}: {book['authors']}")
    else:
        print("No se encontraron libros.")


        
# Step 6: Main function to run the workflow
def main():
    while True:
        print("¿Qué acción desea realizar?")
        print("1. Añadir un libro")
        print("2. Eliminar un libro")
        print("3. Actualizar un libro")
        print("4. Mostrar libros en la base de datos")
        print("5. Salir")
        opcion = input("Ingrese una opción (1-5): ")

        if opcion == '1':
            print("Añadir un libro:")
            print("1. Buscar por ISBN")
            print("2. Buscar por título")
            print("3. Buscar por autor")
            opcion_busqueda = input("Ingrese una opción (1-3): ")

            if opcion_busqueda == '1':
                isbn = input("Ingrese el ISBN del libro: ")
                books = fetch_book_data_isbn(isbn)
                if isinstance(books, list) and books:
                    print("Libro encontrado:")
                    show_books_api(books)
                    seleccion = int(input("Ingrese 1 si es el libro que buscan 0 si no es el libro correcto: ")) - 1
                    if 0 <= seleccion < len(books):
                        # Ask user when they read the book
                        read_date = get_read_date()
                        # Rating the book
                        rate = get_rate()
                        # Number of times readed
                        times_readed = get_times_readed()
                        # Type of book
                        book_type = get_book_format()
                        
                        save_book_to_db(books[seleccion], read_date, rate, times_readed, book_type)
                    else:
                        print("Selección inválida.")
                else:
                    print("No se encontraron libros con ese ISBN.")

            elif opcion_busqueda == '2':
                title = input("Ingrese el título del libro: ")
                books = fetch_book_data_title(title)
                if isinstance(books, list) and books:
                    print("Libros encontrados:")
                    show_books_api(books)
                    seleccion = int(input("Ingrese el número del libro que desea añadir a la base de datos: ")) - 1
                    if 0 <= seleccion < len(books):
                        # Ask user when they read the book
                        read_date = get_read_date()
                        # Rating the book
                        rate = get_rate()
                        # Number of times readed
                        times_readed = get_times_readed()
                        # Type of book
                        book_type = get_book_format()
                        
                        save_book_to_db(books[seleccion], read_date, rate, times_readed, book_type)
                    else:
                        print("Selección inválida.")
                else:
                    print("No se encontraron libros con ese título.")
            
            
            elif opcion_busqueda == '3':
                author = input("Ingrese el nombre del autor: ")
                books = fetch_book_data_author(author)
                if isinstance(books, list) and books:
                    print("Autores encontrados:")
                    show_authors(books)
                    seleccion_author = int(input("Selecciona el autor sobre el que quieres obtener información: ")) -1
                    # Verificar si la selección está dentro del rango
                    if 0 <= seleccion_author < len(books):
                        # Extraer el nombre del autor seleccionado
                        selected_author = books[seleccion_author]['authors']
                        
                        if selected_author:
                            # Buscar libros por el autor seleccionado
                            books_author = fetch_book_data_author(selected_author)
                            
                            if isinstance(books_author, list) and books_author:
                                print("Libros encontrados:")
                                show_books_api(books_author)
                                seleccion = int(input("Ingrese el número del libro que desea añadir a la base de datos: ")) - 1
                                if 0 <= seleccion < len(books_author):
                                    # Ask user when they read the book
                                    read_date = get_read_date()
                                    # Rating the book
                                    rate = get_rate()
                                    # Number of times readed
                                    times_readed = get_times_readed()
                                    # Type of book
                                    book_type = get_book_format()
                                    
                                    save_book_to_db(books_author[seleccion], read_date, rate, times_readed, book_type)
                                else:
                                    print("Selección inválida.")
                            else:
                                print("No se encontraron libros con ese título.")
                        else:
                            print("No se pudo obtener el nombre del autor.")
                    else:
                        print("Selección inválida. Intente de nuevo.")


                    ##if 0 <= seleccion < len(books):
                    ##    # Ask user when they read the book
                    ##    read_date = get_read_date()
                    ##    # Rating the book
                    ##    rate = get_rate()
                    ##    # Number of times readed
                    ##    times_readed = get_times_readed()
                    ##    # Type of book
                    ##    book_type = get_book_format()
                    ##    
                    ##    save_book_to_db(books[seleccion], read_date, rate, times_readed, book_type)
                    ##else:
                    ##    print("Selección inválida.")
                #else:
                #    print("No se encontraron libros con ese título.")

        elif opcion == '2':
            print("Funcionalidad no implementada aún.")
        
        elif opcion == '3':
            print("Funcionalidad no implementada aún.")
        
        elif opcion == '4':
            print("Funcionalidad no implementada aún.")
        
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida. Inténtelo de nuevo.")



if __name__ == "__main__":
    setup_database()
    main()
