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


# Isbn
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
        return None# Isbn

    


def fetch_book_data_isbn(isbn):
    #if check_isbn(isbn) is None:
    #    return print("El ISBN ingresado no es válido. No se realizará la búsqueda.")
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    return fetch_book_data(google_books_api_url, limit=1)
    

def main():
    while True:
        try:
            isbn = input("Ingrese el ISBN del libro: ")
            if isbn.lower() == 'q':
                break   
            elif check_isbn(isbn) is None or check_isbn(isbn) == "Wrong input":
                print("Incorrecto")
                continue
            else:
             books = fetch_book_data_isbn(isbn)
             print(books)
        except ValueError:
                print("\nHa habido un error\n")
                break


main()                    