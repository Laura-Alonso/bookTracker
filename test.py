



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


def check_isbn(col = None):
    if col == '' or col is None:
       return None  
    try:
        col = int(col)
        if len(str(col)) == 13:    
            return col
        else:
            col = "Wrong input"
            return col                
    except ValueError:
        return None
    
    

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




    # PUNTUACIÓN
    elif question == 11:
       while True:
           try:
            new_val = input(f"Puntue el libro del 1 al 5 (pulse 'enter' para dejar vacío o 'q' para salir sin cambios): \n")
            new_val2 = check_rate(new_val)
            if new_val.lower() == "q":
                break
            elif new_val2 == "Wrong input":
                print("\nHas introducido un valor no permitido. Por favor, inténtelo de nuevo. \nRecuerde introducir un número entero del 1 al 5 o pulse enter para dejar vacío\n")
                continue
            
            else:
                con.execute("UPDATE books SET rate = ? WHERE ROWID= ?", (new_val2, int(row)))
                con.commit()
                print(f"La puntuación del libro ha sido actualizado: {new_val2}")
                break            
           except ValueError:
                print("\nHa habido un error\n")
                break