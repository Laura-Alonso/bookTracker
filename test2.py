import requests
import sqlite3
from datetime import datetime


def fetch_book_data_title(title):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(google_books_api_url)
    
    if response.status_code == 200:
        books_info = response.json()
        books = []

        # Sacar la información de los 5 primeros
        for book in books_info.get('items', [])[:5]:
            # Acceder a la información de cada libro a través de 'volumeInfo' y a traves de "industryIdentifiers"
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
            genders = ', '.join(volume_info.get('categories',[]))
            preview_link = volume_info.get('previewLink', 'N/A')
            image_links = image.get('thumbnail', 'N/A')

            # Agregar los detalles a la lista de libros
            books.append({
                'ISBN': isbn,
                'Title': title,
                'Author/s': authors,
                'Description': description,
                'Published date': published_date,
                'Page count': page_count,
                'Language': language,
                'Genders': genders,
                'Preview link': preview_link,
                'Image': image_links
 })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"

 # Función para mostrar los resultados de los libros
def show_books(books):
    if isinstance(books, list):
        for i, books in enumerate(books, 1):
            print(f"Libro {i}:")
            print(f"  Título: {books['Title']}")
            print(f"  Autor(es): {books['Author/s']}")
            print(f"  ISBN: {books['ISBN']}")
            print(f"  Preview link: {books['Preview link']}")

            print('-' * 40)
    else:
        print(books)

# Ejemplo de uso
title_to_search = "centeno"
libros_obtenidos = fetch_book_data_title(title_to_search)
show_books(libros_obtenidos)