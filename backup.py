import requests
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np

# Set up the SQLite database
def setup_database(db_name='personal.db'):
    conn = sqlite3.connect(db_name)  # Establishes a connection to the SQLite database "personal" or create it.
    cursor = conn.cursor()           # Create a cursor object used to execute SQL comands
    
    # Create a table to store book details   # Create SQL comand. Names are columns names.
    cursor.execute('''                        
        CREATE TABLE IF NOT EXISTS books (
            isbn INTEGER,
            title TEXT,
            authors TEXT,
            description TEXT,
            published_date DATE,
            page_count INTEGER,
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
                'isbn': check_isbn(isbn),
                'title': check_string(title),
                'authors': check_string(authors),
                'description': check_string(description),
                'published_date': published_date,
                'page_count': check_integer(page_count),
                'language': check_string(language),
                'genders': check_string(genders),
                'preview_link': check_string(preview_link),
                'image_links': check_string(image_links)
            })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"


# Fetch book data from Google Books API using ISBN

def fetch_book_data_isbn(isbn):
    if check_isbn(isbn) is None:
        return print("El ISBN ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    return fetch_book_data(google_books_api_url, limit=1)
    

# Fetch book data from Google Books API using Title

def fetch_book_data_title(title):
    if check_string(title) is None:
        return print("El título ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    return fetch_book_data(google_books_api_url, limit=5)

# Fetch book data from Google Books API using Author

def fetch_book_data_author(author):
    if check_string(author) is None:
        return print("El autor/es ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    books = fetch_book_data(google_books_api_url, limit=30)
    libros_filtrados = [book for book in books if author in book.get('authors', '')]
    
    return libros_filtrados

# Autores unicos
def fetch_unique_author(author):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    
    autores = set()  # Usamos un conjunto para evitar duplicados automáticamente
    start_index = 0  # Índice inicial para la paginación
    max_results_per_page = 20  # Número máximo de resultados por solicitud (según la API)

    while len(autores) < 10:
        # Actualizar la URL para incluir el parámetro de paginación
        paginated_url = f"{google_books_api_url}&startIndex={start_index}&maxResults={max_results_per_page}"

        # Hacer la solicitud a la API y obtener los datos
        response = requests.get(paginated_url)

        # Verificar si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Convertir la respuesta JSON en un objeto Python
            books_info = response.json()

            # Extraer la lista de libros desde 'items'
            books = books_info.get('items', [])

            # Si no hay más libros, salir del bucle
            if not books:
                break

            # Iterar sobre la lista de libros
            for book in books:
                volume_info = book.get('volumeInfo', {})

                # Obtener la lista de autores, si está disponible
                authors_list = volume_info.get('authors', [])

                # Convertir la lista de autores en una cadena separada por comas
                authors = ', '.join(authors_list)

                # Añadir el autor si es nuevo (el conjunto ya elimina duplicados)
                if authors and len(autores) < 10:
                    autores.add(authors)

                # Detener el bucle si ya tenemos 10 autores
                if len(autores) == 10:
                    break

            # Aumentar el índice para la siguiente página
            start_index += max_results_per_page
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return []

    # Convertir los autores únicos en una lista de diccionarios
    autores_dicts = [{'authors': author} for author in autores]

    return autores_dicts  # Devolver la lista de autores únicos

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
        try:
            times_readed = input("How many times have you read the book? (or leave empty): ")
            return check_integer(times_readed)
        except ValueError:
            break

def get_book_format():
    while True:
        print("Is the book in paper (1) or ebook (2)?")
        book_type = input("Enter 1 for paper, 2 for ebook: ")
        value = check_format(book_type)
        
        if value == 1:
            return 'Paper'  # Retorna 'Paper' si la entrada es válida
        elif value == 2:
            return 'Ebook'  # Retorna 'Ebook' si la entrada es válida
        else:
            print("Entrada no válida. Por favor, introduzca 1 para Papel o 2 para Ebook.")  # Si no es válido, vuelve a pedir

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


# Previsualization of data base
def shows_table_data(db = "personal", tabla = "books"):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')

    df = pd.read_sql_query(f"SELECT rowId as Id, isbn, title, authors,  published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)

    # Obtenemos los resultados
    #print(df)
    print(df.to_markdown(index = False))

    # Cerramos la conexión con la bd
    con.close()


# Download data
def download_data(db = "personal", tabla = "books", formato=None):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')
    formato = formato
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", con)
    df = df.replace({np.nan: None})

    if formato == "1":

        try:

            df.to_csv('database.csv', index=False, encoding='utf-8')
            print("El archivo ha sido guardado correctamente.")

        except PermissionError:
            print("Error: Cierre el archivo en uso antes de descargar una nueva versión.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

        finally:
            # Cerramos la conexión con la bd
            con.close()

    if formato == "2":

        try:

            df.to_csv('database.txt', index=False, encoding='utf-8')
            print("El archivo ha sido guardado correctamente.")

        except PermissionError:
            print("Error: Cierre el archivo en uso antes de descargar una nueva versión.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

        finally:
            # Cerramos la conexión con la bd
            con.close()

    if formato == "3":

        try:

            json_data = df.to_dict(orient="records")
            json_string = json.dumps(json_data, ensure_ascii=False, indent=4)
            with open('database.json', 'w', encoding='utf-8') as f:
                f.write(json_string)
            print("El archivo ha sido guardado correctamente.")

        except PermissionError:
            print("Error: Cierre el archivo en uso antes de descargar una nueva versión.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

        finally:
            # Cerramos la conexión con la bd
            con.close()

# Delete book
def delete_using_db(db = "personal", tabla = "books", row=None, question = None):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')

    df = pd.read_sql_query(f"SELECT rowid AS Id, isbn, title, authors, published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)

    # Obtenemos los resultados
    print(df.to_markdown(index=False))

    # Preguntar que libro quiere borrar
    row = int(input("\nIntroduzca el Id (indetificador) del libro que quieres borrar: "))
    selected_book = df[df['Id'] == row].to_markdown(index=False)
    question = int(input(f"\n¿Estas seguro de que deseas borrar el siguiente libro?: \n\n{selected_book} \n\nSelecciona 1 si estás seguro o 2 si quieres mantenerlo: "))

    # Elegir la fila a eliminar
    con.execute("DELETE FROM books WHERE ROWID={}".format(int(row)))
    if question == 1:
        con.commit()
        print("\nEl libro ha sido borrado\n")
        df_new = pd.read_sql_query(f"SELECT rowid AS Id, isbn, title, authors, published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)
        print(f"\n {df_new.to_markdown(index=False)}\n")
    elif question == 2:
        print("El libro no ha sido borrado\n")    
    else:
        print("\nInvalid input. Please enter 1 for delete or 2 for not delete.\n")
    # Cerramos la conexión con la bd
    con.close()


# Update book data
def update_book(db = "personal", tabla = "books", row=None, question = None):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')

    df = pd.read_sql_query(f"SELECT rowid AS Id, isbn, title, authors, published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)

    # Obtenemos los resultados
    print(df.to_markdown(index=False))

    # Preguntar que libro quiere actualizar
    row = int(input("\nIntroduzca el Id (indetificador) del libro que quieres actualizar: "))
    selected_book = df[df['Id'] == row].to_markdown(index=False)
    campos = {
        "Opción 1": "Isbn",
        "Opción 2": "Título",
        "Opción 3": "Autor/es",
        "Opción 4": "Descripción",
        "Opción 5": "Fecha de publicación (published_date)",
        "Opción 6": "Nº de páginas (page_count)",
        "Opción 7": "Formato",
        "Opción 8": "Idioma",
        "Opción 9": "Genero/s",
        "Opción 10": "Fecha de lectura",
        "Opción 11": "Puntuación",
        "Opción 12": "Número de veces leido"
    }
    campos_legibles = "\n".join([f"{opcion}: {campo}" for opcion, campo in campos.items()])
    question = int(input(f"\n¿Qué campo quieres actualizar (introduzca un número del 1 al 12?: \n\n{campos_legibles} \n\n"))

    # ISBN
    if question == 1:
        while True:
            new_val = input(f"\nIntroduzca el nuevo ISBN (solo números): \n\n")
            if check_isbn(new_val) is None:
                print("\nInvalid input. Por favor, introduzca solo números sin espacios ni guiones.\n")
            else:
                con.execute("UPDATE books SET ISBN = ? WHERE ROWID= ?", (new_val, int(row)))
                con.commit()
                print(f"El ISBN ha sido actualizado a: {new_val}")
                break

    # TÍTULO
    elif question == 2:
       while True:
           new_val = str(input(f"\nIntroduzca el nuevo título: \n\n"))
           if check_string(new_val) is None:
               print("\nInvalid input. Por favor, introduzca una cadena de texto.\n")
           else:
               con.execute("UPDATE books SET title = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El título ha sido actualizado a: {new_val}")
               break


    # AUTORES
    elif question == 3:
       while True:
           new_val = str(input(f"\nIntroduzca el nuevo autor. \nSi hay más de un autor, sepárelos por comas (Luis Rojas, Eloy Moreno).\nTenga en cuenta que todos los autores anteriores se perderan. \nNuevo/s autor/es: \n"))
           if check_string(new_val) is None:
               print("\nInvalid input. Por favor, introduzca una cadena de texto.\n")
           else:
               con.execute("UPDATE books SET authors = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo autores ha sido actualizado a: {new_val}")
               break


    # DESCRIPCIÓN
    elif question == 4:
       while True:
           new_val = str(input(f"\nIntroduzca una descripción sobre el libro. \nTenga en cuenta que la descripción antrior se perdera. \nDescripción: \n"))
           if check_string(new_val) is None:
               print("\nInvalid input. Por favor, introduzca una cadena de texto.\n")
           else:
               con.execute("UPDATE books SET description = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"La descripción ha sido actualizada: {new_val}")
               break

    # FECHA DE PUBLICACIÓN
    elif question == 5:
       while True:
           new_val = str(input(f"\nIntroduzca la nueva fecha de publicación (Formato YYYY-MM-DD. Si no sabe el año, el mes o el día sustituye con unos): \n"))
           try:
               datetime.strptime(new_val, "%Y-%m-%d")
               con.execute("UPDATE books SET published_date = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"La fecha de publicación ha sido actualizada: {new_val}")
               break
           except ValueError:
               print("\nInvalid input. Por favor, inténtelo de nuevo. Recuerde usar el formato YYYY-MM-DD.Si no sabe el año, el mes o el día sustituye con unos\n")
               break

    # NÚMERO DE PÁGINAS
    elif question == 6:
       while True:
           new_val = input(f"\nIntroduzca el númereo de páginas: \n")
           new_value = check_integer(new_val)
           if new_val is None:
               print("\nInvalid input. Por favor, introduzca uun número válido.\n")
           else:   
               con.execute("UPDATE books SET page_count = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El número de páginas ha sido actualizado: {new_val}")
               break
    
    # FORMATO
    elif question == 7:
       while True:
         new_val = input(f"\nIntroduzca el formato del libro. Introduzca 1 para formato papel, 2 para formato ebook: \n")
         new_value = check_format(new_val)
         if new_value is None:
             print("\nInvalid input. or favor, introduzca 1 para formato papel, 2 para formato ebook, o 'q' para salir.\n")
             break
         elif new_value == 1: 
             con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("Paper", int(row)))
             con.commit()
             print(f"El libro ha sido actualizado a formato papel")
             break
         elif new_value == 2:
             con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("Ebook", int(row)))
             con.commit()
             print(f"El libro ha sido actualizado a formato ebook")
             break  
         else:
             break  
           
    # IDIOMA
    elif question == 8:
       while True:
           new_val  = str(input(f"\nIntroduzca las dos primeras iniciales del idioma del libro (Ejemplo: Español --> es, Portugues --> pt):  \n"))
           new_val2 = str(input(f"\nSi quiere especificar el país de origen introduzca las dos primeras iniciales del país (Ejemplo: Argentina --> ar, Brasil --> br)\nSi no quiere especificar nada, pulse 0.\nPaís: \n"))

           if len(new_val) == 2 and len(new_val2) == 2:
               final_value = new_val + " - " + new_val2
               con.execute("UPDATE books SET language = ? WHERE ROWID= ?", (final_value, int(row)))
               con.commit()
               print(f"El idioma ha sido actualizada: {final_value}")
               break
           elif len(new_val) == 2 and len(new_val2) == 1: 
               final_value = new_val
               con.execute("UPDATE books SET language = ? WHERE ROWID= ?", (final_value, int(row)))
               con.commit()
               print(f"El idioma ha sido actualizada: {final_value}")
               break
           else:
               print("Se ha producido un error")
               break

    # GÉNERO/S
    elif question == 9:
       while True:
           new_val = str(input(f"\nIntroduzca el género del libro. \nSi hay más de un género, sepárelos por comas (Ficción, Romance).\nTenga en cuenta que los géneros anteriores se perderan. \nNuevo/s género/s: \n"))
           if check_string(new_val) is None:
               print("\nInvalid input. Por favor, introduzca una cadena de texto.\n")
           else:
               con.execute("UPDATE books SET genders = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo género del libro ha sido actualizado a: {new_val}")
               break
                         

    # FECHA DE LECTURA
    elif question == 10:
       while True:
           new_val = str(input(f"\nIntroduzca la fecha de lectura (Formato YYYY-MM-DD. Si no sabe el año, el mes o el día sustituye con unos): \n"))
           try:
               datetime.strptime(new_val, "%Y-%m-%d")
               con.execute("UPDATE books SET read_date = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"La fecha de lectura ha sido actualizada: {new_val}")
               break
           except ValueError:
               print("\nInvalid input. Por favor, inténtelo de nuevo. Recuerde usar el formato YYYY-MM-DD.Si no sabe el año, el mes o el día sustituye con unos\n")
               break

    # PUNTUACIÓN
    elif question == 11:
       while True:
           new_val = int(input(f"\nIntroduzca la puntuación que quiere asignar al libro (valores enteros del 0 al 5): \n"))
           if type(new_val) == int and new_val in [0,1,2,3,4,5]:
               con.execute("UPDATE books SET rate = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El puntuación del libro ha sido actualizado: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo. Recuerde introducir un número entero del 0 al 5\n")
               break

    # NÚMERO DE VECES LEIDO
    elif question == 12:
       while True:
           new_val = input(f"\nIntroduzca el número de veces que ha leido el libro (valores enteros): \n")
           new_value = check_integer(new_val)
           if new_value is None:
               print("\nInvalid input. Por favor, inténtelo de nuevo. Recuerde introducir un número entero\n")
           else:    
               con.execute("UPDATE books SET times_readed = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo número de veces que ha leido el libro ha sido actualizado: {new_val}")
               break
           
    # Cerramos la conexión con la bd
    con.close() 



### CHEQUEOS FORMATO

# Isbn
def check_isbn(col = None):
     while True:
        if col == '' or col is None:
            return None  # Permite un valor nulo
        try:
            col = int(col)
            if len(str(col)) == 13:    
                return col
            else:
                 print("El ISBN debe ser un número de 13 dígitos.")
                 break                 
        except ValueError:
            print("El ISBN debe ser un número de 13 dígitos.")
            break

# String (title, authors, description, gender, preview_link, image_lin)
def check_string(col = None):
    while True:
        if col == "" or col is None:
            return None
        try:
            col = str(col)
            return col
        except ValueError:
            print("Debe ser una cadena de texto")
            break

# Integer (page_count, times_readed)
def check_integer(col = None):
    while True:
        if col == '' or col is None:
           return None  # Permite un valor nulo 
        try:
            col = int(col)
            return col
        except ValueError:
            print("Solo se permite introducir números")
            col = input("Por favor, introduzca un número: ")

# Format
def check_format(col = None):
    while True:
        if col == '' or col is None:
            return None  # Permite un valor nulo
        try:
            col = int(col)
            if col in (1,2):    
                return col 
            else:
                break            
        except ValueError:
            print("Debe ser un número 1 o 2")
            col = input("Por favor, introduzca un número: ")   


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
                if fetch_book_data_isbn(isbn) is None:
                    break
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
                if fetch_book_data_title(title) is None:
                    break
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
                if fetch_book_data_title(author) is None:
                    break
                books = fetch_book_data_author(author)
                autores = fetch_unique_author(author)
                if isinstance(autores, list) and autores:
                    print("Autores encontrados:")
                    show_authors(autores)
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

        elif opcion == '2':
            delete_using_db()
        
        elif opcion == '3':
            update_book()
        
        elif opcion == '4':
            print("Elija una acción:")
            print("1. Previsualizar la base de datos")
            print("2. Descargar la base de datos")
            opcion_busqueda = input("Ingrese una opción (1-2): ")

            if opcion_busqueda == '1':
                shows_table_data()
            if opcion_busqueda == '2':
                print("Elija un formato:")
                print("1. csv")
                print("2. txt")
                print("3. json")
                opcion_busqueda = input("Ingrese una opción (1-3): ")
                download_data(formato = opcion_busqueda)
        
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida. Inténtelo de nuevo.")



if __name__ == "__main__":
    setup_database()
    main()
