import requests
import sqlite3
import json
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import json
# Obtener datos de los libro
def download_data(db = "personal", tabla = "books", formato=None):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')
    formato = formato
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", con)

    if formato == "csv":

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

    if formato == "txt":

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

    if formato == "csv":

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

    if formato == "json":

        try:

            json_string = json.dumps(df.values.tolist(), ensure_ascii=False, indent=4)
            with open('database.json', 'w', encoding='utf-8') as f:
                f.write(json_string)

        except PermissionError:
            print("Error: Cierre el archivo en uso antes de descargar una nueva versión.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

        finally:
            # Cerramos la conexión con la bd
            con.close()

download_data(formato = "json")


