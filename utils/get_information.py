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
        print("Is the book in paper (1) or ebook (2)?")
        book_type = input("Enter 1 for paper, 2 for ebook: ")
        value = check_format(book_type)
        
        if value == 1:
            return 'Paper'  # Retorna 'Paper' si la entrada es válida
        elif value == 2:
            return 'Ebook'  # Retorna 'Ebook' si la entrada es válida
        else:
            print("Entrada no válida. Por favor, introduzca 1 para Papel o 2 para Ebook.")  # Si no es válido, vuelve a pedir