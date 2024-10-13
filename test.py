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
        "Opción 1": "isbn",
        "Opción 2": "title",
        "Opción 3": "authors",
        "Opción 4": "description",
        "Opción 5": "published_date",
        "Opción 6": "page_count",
        "Opción 7": "formato",
        "Opción 8": "language",
        "Opción 9": "genders",
        "Opción 10": "read_date",
        "Opción 11": "rate",
        "Opción 12": "times_readed"
    }
    campos_legibles = "\n".join([f"{opcion}: {campo}" for opcion, campo in campos.items()])
    question = int(input(f"\n¿Qué campo quieres actualizar (introduzca XXXX?: \n\n{campos_legibles} \n\n"))

    ## Elegir la fila a eliminar
    #con.execute("DELETE FROM books WHERE ROWID={}".format(int(row)))
    #if question == 1:
    #    con.commit()
    #    print("\nEl libro ha sido borrado\n")
    #    df_new = pd.read_sql_query(f"SELECT rowid AS Id, isbn, title, authors, published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)
    #    print(f"\n {df_new.to_markdown(index=False)}\n")
    #elif question == 2:
    #    print("El libro no ha sido borrado\n")    
    #else:
    #    print("\nInvalid input. Please enter 1 for delete or 2 for not delete.\n")
    ## Cerramos la conexión con la bd
    #con.close()

update_book()


