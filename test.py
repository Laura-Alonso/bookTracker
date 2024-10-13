import requests
import sqlite3
import json
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import json
import numpy as np

# Download data
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
            try:
                new_val = int(input(f"\nIntroduzca el nuevo ISBN (solo números): \n\n"))
                if type(new_val) == int:
                    con.execute("UPDATE books SET ISBN = ? WHERE ROWID= ?", (new_val, int(row)))
                    con.commit()
                    print(f"El ISBN ha sido actualizado a: {new_val}")
                    break
            except ValueError:
                print("\nInvalid input. Por favor, introduzca solo números sin espacios ni guiones.\n")
                break

    # TÍTULO
    elif question == 2:
       while True:
           new_val = str(input(f"\nIntroduzca el nuevo título: \n\n"))
           if type(new_val) == str:
               con.execute("UPDATE books SET title = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El título ha sido actualizado a: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo.\n")
               break   

    # AUTORES
    elif question == 3:
       while True:
           new_val = str(input(f"\nIntroduzca el nuevo autor. \nSi hay más de un autor, sepárelos por comas (Luis Rojas, Eloy Moreno).\nTenga en cuenta que todos los autores anteriores se perderan. \nNuevo/s autor/es: \n"))
           if type(new_val) == str:
               con.execute("UPDATE books SET authors = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo autores ha sido actualizado a: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo.\n") 
               break

    # DESCRIPCIÓN
    elif question == 4:
       while True:
           new_val = str(input(f"\nIntroduzca una descripción sobre el libro. \nTenga en cuenta que la descripción antrior se perdera. \nDescripción: \n"))
           if type(new_val) == str:
               con.execute("UPDATE books SET description = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"La descripción ha sido actualizada: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo.\n") 
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
           new_val = int(input(f"\nIntroduzca el númreo de páginas: \n"))
           if type(new_val) == int:
               con.execute("UPDATE books SET page_count = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El número de páginas ha sido actualizado: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo.\n")
               break
    
    # FORMATO
    elif question == 7:
       while True:
         new_val = int(input(f"\nIntroduzca el formato del libro. Introduzca 1 para formato papel, 2 para formato ebook: \n"))
         if type(new_val) == int and new_val == 1:
             con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("Paper", int(row)))
             con.commit()
             print(f"El libro ha sido actualizado a formato papel")
             break
         elif type(new_val) == int and new_val == 2:
             con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("Ebook", int(row)))
             con.commit()
             print(f"El libro ha sido actualizado a formato ebook")
             break   
         else:
          # Entrada inválida si el valor no es ni 1 ni 2
          print("\nEntrada inválida. Por favor, introduzca 1 para formato papel, 2 para formato ebook, o 'q' para salir.\n")    
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
           if type(new_val) == str:
               con.execute("UPDATE books SET genders = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo género del libro ha sido actualizado a: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo.\n")
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
           new_val = int(input(f"\nIntroduzca el número de veces que ha leido el libro (valores enteros): \n"))
           if type(new_val) == int:
               con.execute("UPDATE books SET times_readed = ? WHERE ROWID= ?", (new_val, int(row)))
               con.commit()
               print(f"El campo número de veces que ha leido el libro ha sido actualizado: {new_val}")
               break
           else:
               print("\nInvalid input. Por favor, inténtelo de nuevo. Recuerde introducir un número entero\n")
               break
           
    # Cerramos la conexión con la bd
    con.close()      


update_book()


