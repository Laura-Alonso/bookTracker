import requests

def fetch_unique_author(author):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    
    autores = set()  # Usamos un conjunto para evitar duplicados automáticamente
    start_index = 0  # Índice inicial para la paginación
    max_results_per_page = 40  # Número máximo de resultados por solicitud (según la API)

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
                if authors:
                    autores.add(authors)

            # Aumentar el índice para la siguiente página
            start_index += max_results_per_page
        else:
            print(f"Error en la solicitud: {response.status_code}")
            return []

    # Convertir los autores únicos en una lista de diccionarios
    autores_dicts = [{'authors': author} for author in autores]

    return autores_dicts  # Devolver la lista de autores únicos


# Ejemplo de uso
print(fetch_unique_author("Ruben"))
