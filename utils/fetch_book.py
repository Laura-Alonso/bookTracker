import requests
from utils.check import * 

# Obtener datos de los libro
def fetch_book_data(api_url, limit=None):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        books_info = response.json()
        books = []

        # Obtener los libros (todos o con límite)
        items = books_info.get('items', [])
        if limit is not None:
            items = items[:limit]

        # Acceder a la información de cada libro
        for book in items:
            volume_info = book.get('volumeInfo', {})
            identifiers = volume_info.get('industryIdentifiers', [])
            image = volume_info.get('imageLinks', {})

            # Extraer la información
            isbn = next((identifier['identifier'] for identifier in identifiers if identifier['type'] == 'ISBN_13'), 'N/A')
            title = volume_info.get("title", "N/A")
            authors = ', '.join(volume_info.get('authors', []))
            description = volume_info.get('description', 'N/A')
            published_date = volume_info.get('publishedDate', 'N/A')
            page_count = volume_info.get('pageCount', 'N/A')
            language = volume_info.get('language', 'N/A')
            genders = ', '.join(volume_info.get('categories', []))
            preview_link = volume_info.get('previewLink', 'N/A')
            image_links = image.get('thumbnail', 'N/A')

            # Agregar los detalles a la lista de libros
            books.append({
                'isbn': check_isbn(isbn),
                'title': check_string(title),
                'authors': check_string(authors),
                'description': check_string(description),
                'published_date': check_date(published_date),
                'page_count': check_integer(page_count),
                'language': check_string(language),
                'genders': check_string(genders),
                'preview_link': check_string(preview_link),
                'image_links': check_string(image_links)
            })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"


# Fetch book data from Google Books API using ISBN

def fetch_book_data_isbn(isbn):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    return fetch_book_data(google_books_api_url, limit=1)
    

# Fetch book data from Google Books API using Title

def fetch_book_data_title(title):
    if check_string(title) is None:
        return print("El título ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    return fetch_book_data(google_books_api_url, limit=5)

# Fetch book data from Google Books API using Author

def fetch_book_data_author(author):
    if check_string(author) is None:
        return print("El autor/es ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    books = fetch_book_data(google_books_api_url, limit=30)
    libros_filtrados = [book for book in books if author in book.get('authors', '')]
    
    return libros_filtrados

# Autores unicos
def fetch_unique_author(author):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    
    autores = set()  # Usamos un conjunto para evitar duplicados automáticamente
    start_index = 0  # Índice inicial para la paginación
    max_results_per_page = 20  # Número máximo de resultados por solicitud (según la API)

    while len(autores) < 10:
        # Actualizar la URL para incluir el parámetro de paginación
        paginated_url = f"{google_books_api_url}&startIndex={start_index}&maxResults={max_results_per_page}"

        # Hacer la solicitud a la API y obtener los datos
        response = requests.get(paginated_url)

        # Verificar si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Convertir la respuesta JSON en un objeto Python
            books_info = response.json()

            # Extraer la lista de libros desde 'items'
            books = books_info.get('items', [])

            # Si no hay más libros, salir del bucle
            if not books:
                break

            # Iterar sobre la lista de libros
            for book in books:
                volume_info = book.get('volumeInfo', {})

                # Obtener la lista de autores, si está disponible
                authors_list = volume_info.get('authors', [])

                # Convertir la lista de autores en una cadena separada por comas
                authors = ', '.join(authors_list)

                # Añadir el autor si es nuevo (el conjunto ya elimina duplicados)
                if authors and len(autores) < 10:
                    autores.add(authors)

                # Detener el bucle si ya tenemos 10 autores
                if len(autores) == 10:
                    break

            # Aumentar el índice para la siguiente página
            start_index += max_results_per_page
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return []

    # Convertir los autores únicos en una lista de diccionarios
    autores_dicts = [{'authors': author} for author in autores]

    return autores_dicts  # Devolver la lista de autores únicos