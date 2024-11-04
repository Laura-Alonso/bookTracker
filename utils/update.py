from utils.check import * 
import pandas as pd
import sqlite3

# Update isbn
def update_book_isbn(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
            try:
                new_val = input(f"Ingrese el ISBN del libro (número de 13 dígitos). \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
                new_val2 = check_isbn(new_val)
                if new_val.lower() == "q":
                    break
                elif new_val2 == "Wrong input":
                  print("\nEntrada no válida. Por favor, inténtelo de nuevo.")
                else:
                  con.execute("UPDATE books SET ISBN = ? WHERE ROWID= ?", (new_val2, int(row)))
                  con.commit()
                  print(f"El ISBN ha sido actualizado a: {new_val2}")
                  break
            except ValueError:
                print("\nHa habido un error\n")
                break
 

# Update title
def udpate_book_title(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
               new_val = input(f"Introduzca el nuevo título. \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
               new_val2 = check_string(new_val)
               if new_val.lower() == "q":
                    break
               elif new_val2 == "Wrong input":
                  print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
               else:
                con.execute("UPDATE books SET title = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"El título ha sido actualizado a: {new_val2}")
               break
           except ValueError:
                print("\nHa habido un error\n")
                break
           #finally:
            #    con.close()

# Update author/s
def udpate_book_author(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
               new_val = input(f"Introduzca el nuevo autor. Si hay más de un autor, sepárelos con comas (Luis Rojas, Eloy Moreno).\nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
               new_val2 = check_string(new_val)
               if new_val.lower() == "q":
                    break
               elif new_val2 == "Wrong input":
                  print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
               else:
                con.execute("UPDATE books SET authors = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"El campo autores ha sido actualizado a: {new_val2}")
               break
           except ValueError:
                print("\nHa habido un error\n")
                break



# Update description
def udpate_book_description(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
               new_val = input(f"Introduzca una descripción sobre el libro. \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
               new_val2 = check_string(new_val)
               if new_val.lower() == "q":
                    break
               elif new_val2 == "Wrong input":
                  print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
               else:
                con.execute("UPDATE books SET description = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"La descripción ha sido actualizada a: {new_val2}")
               break
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update publish date
def udpate_book_publish_date(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
              new_val = input(f"Introduzca la nueva fecha de publicación en formato YYYY-MM-DD. Si no sabe el mes o el día sustitúyalos por '01'). \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
              new_val2 = check_date(new_val)
              if new_val.lower() == "q":
                   break
              elif new_val2 == "Wrong input":
                     print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
              else:
                  con.execute("UPDATE books SET published_date = ? WHERE ROWID= ?", (new_val2, int(row)))
                  con.commit()
                  print(f"La fecha de publicación ha sido actualizada a: {new_val2}")
                  break
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update page count
def udpate_book_page_count(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
              new_val = input(f"Introduzca el número de páginas.\nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
              new_val2 = check_integer(new_val)
              if new_val.lower() == "q":
                   break
              elif new_val2 == "Wrong input":
                     print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
              else:
                  con.execute("UPDATE books SET page_count = ? WHERE ROWID= ?", (new_val2, int(row)))
                  con.commit()
                  print(f"El número de páginas ha sido actualizado a: {new_val2}")
                  break
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update book format
def udpate_book_format(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
         try:
             new_val = input(f"Introduzca el formato del libro. Introduzca '1' para formato papel, '2' para formato e-book. \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
             new_val2 = check_format(new_val)
             if new_val.lower() == "q":
                   break
             elif new_val2 == "Wrong input":
                     print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
             elif new_val2 == 1:
                  con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("Papel", int(row)))
                  con.commit()
                  print(f"El libro ha sido actualizado a formato papel")
                  break
             elif new_val2 == 2:
                  con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", ("E-book", int(row)))
                  con.commit()
                  print(f"El libro ha sido actualizado a formato e-book")
                  break
             else:
                 con.execute("UPDATE books SET formato = ? WHERE ROWID= ?", (new_val2, int(row)))
                 con.commit()
                 print(f"El formato del libro ha sido actualizado a: {new_val2}")
                 break
         except ValueError:
            print("\nHa habido un error\n")
            break


# Update language
def udpate_book_language(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
             new_val  = input(f"Introduzca las dos primeras iniciales del idioma del libro en minúsculas (Ejemplo: Español --> es, Portugues --> pt).\nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
             
             if new_val.lower() == "q":
                   break
             elif new_val == '':
                final_value = None
                con.execute("UPDATE books SET language = ? WHERE ROWID= ?", (final_value, int(row)))
                con.commit() 
                print(f"El idioma ha sido actualizado a: {final_value}")
                break
             
             elif len(new_val) == 2:
                 while True:
                    try:

                        new_val2 = input(f"Si quiere especificar el país de origen, introduzca las dos primeras iniciales del país en mayúsculas (Ejemplo: Argentina --> AR, Brasil --> BR). \nSi no quiere especificar nada, pulse 'enter'.\n")
                        if len(new_val) == 2 and len(new_val2) == 2:
                           final_value = new_val.lower() + "-" + new_val2.upper()
                           con.execute("UPDATE books SET language = ? WHERE ROWID= ?", (final_value, int(row)))
                           con.commit()
                           print(f"El idioma ha sido actualizado a: {final_value}")
                           break
                        
                        elif len(new_val) == 2 and len(new_val2) == 0: 
                           final_value = new_val.lower()
                           con.execute("UPDATE books SET language = ? WHERE ROWID= ?", (final_value, int(row)))
                           con.commit()
                           print(f"El idioma ha sido actualizada a: {final_value}")
                           break
                        else:
                           print("Entrada no válida. Por favor, inténtelo de nuevo.")
                    except ValueError:
                       print("\nHa habido un error\n")
                       break
                 break
             else:
                 print("Entrada no válida. Por favor, inténtelo de nuevo.")
        
           except ValueError:
             print("\nHa habido un error\n")
             break


# Update gender
def udpate_book_gender(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
               new_val = input(f"Introduzca el género del libro. Si hay más de un género, sepárelos comas comas (Ficción, Romance).\nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
               new_val2 = check_string(new_val)
               if new_val.lower() == "q":
                    break
               elif new_val2 == "Wrong input":
                  print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
               else:
                con.execute("UPDATE books SET genders = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"El campo género ha sido actualizado a: {new_val2}")
               break
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update reading date
def udpate_book_reading_date(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
             new_val = input(f"Introduzca la nueva fecha de lectura en formato YYYY-MM-DD. Si no sabe el mes o el día sustitúyalos por '01'). \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
             new_val2 = check_date(new_val)
             if new_val.lower() == "q":
                  break
             elif new_val2 == "Wrong input":
                       print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
             else:
                 con.execute("UPDATE books SET read_date = ? WHERE ROWID= ?", (new_val2, int(row)))
                 con.commit()
                 print(f"La fecha de lectura ha sido actualizada a: {new_val2}")
                 break
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update rate
def udpate_book_rate(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
            new_val = input(f"Puntue el libro del 1 al 5.\nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
            new_val2 = check_rate(new_val)
            if new_val.lower() == "q":
                break
            elif new_val2 == "Wrong input":
                print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
            else:
                con.execute("UPDATE books SET rate = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"La puntuación del libro ha sido actualizada a: {new_val2}")
                break            
           except ValueError:
                print("\nHa habido un error\n")
                break


# Update times readed
def udpate_book_times_readed(db="personal", table ="books", row = None):
        con = sqlite3.connect(f'./{db}.db')
        while True:
           try:
              new_val = input(f"Introduzca el número de veces que ha leido el libro (valores enteros). \nTenga en cuenta que la información anterior se perderá. \nPuede pulsar 'enter' para dejar vacío o escribir 'q' para salir: ")
              new_val2 = check_integer(new_val)
              if new_val.lower() == "q":
                   break
              elif new_val2 == "Wrong input":
                     print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
              else:
                   con.execute("UPDATE books SET times_readed = ? WHERE ROWID= ?", (new_val2, int(row)))
                   con.commit()
                   print(f"El número de veces que ha leido el libro ha sido actualizado a: {new_val2}")
                   break
           except ValueError:
                print("\nHa habido un error\n")
                break



