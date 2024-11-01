from datetime import datetime

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

# Date
def check_date(col=None):
    # Solo valida el formato; no pide más entradas
    if col == '' or col is None:
        return None  # Permite un valor nulo
    elif len(col) == 4:
        col2 = f"{col}-01-01"
    else:
        col2 = col
    try:
        col2 = datetime.strptime(col2, '%Y-%m-%d').date()
        return col2
    except ValueError:
        return None  # Devuelve None si no es un número

# Rate    
def check_rate(col=None):
    if col == '' or col is None:
        return None
    try:
        col = int(col)
        if col in (1, 2, 3, 4, 5):
            return col  # Return valid rating
        else:
            col = "Wrong input"
            return col
    except ValueError:
        return None