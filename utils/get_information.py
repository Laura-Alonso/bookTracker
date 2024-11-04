from utils.check import * 


def get_read_date():
    while True:
        read_date = input("\n¿Cuándo leiste el libro por primera vez? Introduzca la fecha con el siguiente formato: YYYY-MM-DD. Si no sabe el mes o el día sustitúyalos por '01').\nPulse 'enter' para dejar este campo vacío:  ")
        try:
            if check_date(read_date) == "Wrong input":
                print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
            else:
                return check_date(read_date)
        except ValueError:
            print("\nHa habido un error\n")
            break

def get_rate():
    while True:
        rate = input("\nPuntue el libro del 1 al 5. \nPulse 'enter' para dejar este campo vacío:  ")
        try:
            if check_rate(rate) == "Wrong input":
                print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
            else:
                return check_rate(rate)
        except ValueError:
            print("\nHa habido un error\n")
            break



def get_times_readed():
    while True:
        times_readed = input("\n¿Cuántas veces has leído el libro?\nPulse 'enter' para dejar este campo vacío:  ")
        try:
            if check_integer(times_readed) == "Wrong input":
                print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
            else:
                return check_integer(times_readed)          
        except ValueError:
            print("\nHa habido un error\n")
            break


def get_book_format():
    while True:
        book_type = input("\n¿Has leído el libro en formato papel (1) o en formato e-book (2). \nPulse 'enter' para dejar este campo vacío:  ")
        try:
            if check_format(book_type) == "Wrong input":
                print("\nEntrada no válida. Por favor, inténtelo de nuevo.\n")
            elif check_format(book_type) == 1:
                return 'Papel' 
            elif check_format(book_type) == 2:
                return 'E-book' 
            else:
                return None 
        except ValueError:
            print("\nHa habido un error\n")
            break