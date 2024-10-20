def check_isbn(col=None):
    # Validar si el ISBN es nulo o vacío
    if col == '' or col is None:
        print("Error: ISBN no puede estar vacío o nulo.")
        return None
    
    try:
        # Convertir a entero
        col = int(col)
        # Verificar si tiene 13 dígitos
        if len(str(col)) == 13:
            return col
        else:
            print("Error: ISBN debe ser un número de 13 dígitos.")
            return None
    except ValueError:
        print("Error: El ISBN debe ser un número.")
        return None

# Función para obtener los datos del libro usando ISBN
def fetch_book_data_isbn(isbn):
    # Validar ISBN antes de hacer la petición
    valid_isbn = check_isbn(isbn)
    
    if valid_isbn is None:
        print("El ISBN ingresado no es válido. No se realizará la búsqueda.")
        return  # Si el ISBN no es válido, detener la función
    
    # Si el ISBN es válido, realizar la solicitud a la API
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{valid_isbn}"
    return fetch_book_data(google_books_api_url, limit=1)

# Ejemplo de uso:
fetch_book_data_isbn('1234567890123')  # ISBN válido de ejemplo
fetch_book_data_isbn('123')            # ISBN inválido de ejemplo
