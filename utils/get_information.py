from utils.check import * 


def get_read_date():
    while True:
        read_date = input("¿Cuándo leiste el libro por primera vez? Introduzca la fecha con el siguiente formato: YYYY-MM-DD o pulse 'enter' para dejar vacío: ")
        try:
            if check_date(read_date) == "Wrong input":
                print("\nHas introducido un valor no permitido. Por favor, inténtelo de nuevo. \nRecuerde introducir una fecha con el formato YYYY-MM-DD")
                continue
            return check_date(read_date)
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format or leave empty.")

def get_rate():
    while True:
        rate = input("Puntue el libro del 1 al 5 (pulse enter para dejar vacío): ")
        try:
            if check_rate(rate) == "Wrong input":
                print("\nHas introducido un valor no permitido. Por favor, inténtelo de nuevo. \nRecuerde introducir un número entero del 1 al 5 o pulse enter para dejar vacío")
                continue
            else:
                return check_rate(rate)
        except ValueError:
            break



def get_times_readed():
    while True:
        try:
            times_readed = input("How many times have you read the book? (or leave empty): ")
            return check_integer(times_readed)
        except ValueError:
            break

def get_book_format():
    while True:
        book_type = input("¿El libro es en formato papel (1) o e-book (2). Pulse 'enter' para dejar vacío.")
        try:
            if check_format(book_type) == "Wrong input":
                print("\nHas introducido un valor no permitido. Por favor, inténtelo de nuevo. \nRecuerde introducir 1 para formato papel, 2 para formato e-book")
                continue
            elif check_format(book_type) == 1:
                return 'Papel' 
            elif check_format(book_type) == 2:
                return 'E-book' 
            else:
                return None 
        except ValueError:
            break