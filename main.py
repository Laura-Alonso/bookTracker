
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np
from utils.check import * 
from utils.fetch_book import * 
from utils.update import *
from utils.get_information import *
from utils.principal_functions import *


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
    print(df.to_markdown(index = False, floatfmt=".0f"))

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
    row = int(input("\nIntroduzca el Id (idetificador) del libro que quieres borrar: "))
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
                while True:
                    try:
                        isbn = input("Ingrese el ISBN del libro (número de 13 dígitos). \n Escriba 'q' para salir: ")
                        if isbn.lower() == 'q':
                            break   
                        elif check_isbn(isbn) is None or check_isbn(isbn) == "Wrong input":
                            print("ISBN incorrecto.")
                            continue
                        else:
                            books = fetch_book_data_isbn(isbn)
                            break
                    except ValueError:
                        print("\nHa habido un error\n")
                        break
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
