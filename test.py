import requests
import sqlite3
from datetime import datetime


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
                'isbn': isbn,
                'title': title,
                'authors': authors,
                'description': description,
                'published_date': published_date,
                'page_count': page_count,
                'language': language,
                'genders': genders,
                'preview_link': preview_link,
                'image_links': image_links
            })
        
        return books
    else:
        return f"Request error. Status code: {response.status_code}"


def fetch_book_data_author(author):

    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}"
    books = fetch_book_data(google_books_api_url, limit=30)
    libros_filtrados = [book for book in books if author in book.get('authors', '')]
    
    return libros_filtrados

    #return books


#print(fetch_book_data("https://www.googleapis.com/books/v1/volumes?q=inauthor:Carmen%20Bravo-Villasante"))
print(fetch_book_data_author("Carmen Bravo-Villasante"))