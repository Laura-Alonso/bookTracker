# Description
Keep track of the books you've read, store general information such as ISBN, title, description, etc., and add individual information like your own rating, reading date, etc. Have all the information about your books collected in one place.

# Fields

|Column         | Origin     |  Path API                             | Type    | Especific format  | Checked?  | 
|---------------|------------|---------------------------------------|---------|-------------------|-----------|
|isbn           | Input, API |                                       | INT     | lenght 13         |    [X]    |
|title          | Input, API |                                       | STRING  |                   |    [X]    |
|authors        | Input, API |                                       | STRING  |                   |    [X]    |
|description    | API        | items.description                     | STRING  |                   |    [X]    |
|published_date | API        |                                       | DATE    |                   |    [X]    |
|page_count     | API        | items.volumeInfo.pageCount            | INT     |                   |    [X]    |
|formato        | Input      |                                       | STRING  | 1. Papel 2. Ebook |    [X]    |
|languaje       | API        | items.volumeInfo.language             | STRING  |                   |    [X]     |
|genders        | API        | items.volumeInfo.categories           | STRING  |                   |    [X]    |
|image_links    | API        | items.volumeInfo.imageLinks.thumbnail | STRING  |                   |    [X]    |
|preview_link   | API        | items.volumeInfo.previewLink          | STRING  |                   |    [X]    |
|read_date      | Input      |                                       | DATE    |                   |    [X]    |
|rate           | Input      |                                       | INT     |                   |    [X]    |
|times_readed   | Input      |                                       | INT     |                   |    [X]    |


# Functions

| Command                                                                            | Description                                       | In main script ? |
|------------------------------------------------------------------------------------|---------------------------------------------------|------------------|
|def setup_database(db_name='personal.db')                                           | Set up the SQLite database                        | Yes              |
|def fetch_book_data(api_url, limit=None)                                            | Fetch book information                            | Yes              |
|def fetch_book_data_isbn(isbn)                                                      | Fetch book data from Google Books API using ISBN  | Yes              |
|def fetch_book_data_title(title)                                                    | Fetch book data from Google Books API using Tile  | Yes              |
|def fetch_book_data_author(author)                                                  | Fetch book data from Google Books API using Author| Yes              |
|def show_books_api(books)                                                           | Show books information                            | Yes              |
|def get_read_date()                                                                 | Get read_date information                         | Yes              |
|def get_rate()                                                                      | Get rate information                              | Yes              |
|def get_times_readed()                                                              | Get times readed                                  | Yes              |
|def get_book_format()                                                               | Get book format                                   | Yes              |
|save_book_to_db(book, read_date, rate, times_readed, formato, db_name='personal.db')| Save book data to database                        | Yes              |
|book_exists(isbn, db_name='personal.db')                                            | Check if the book already exists in the database  | Yes              |
|def ask_updates(isbn, db_name='personal.db')                                        | Ask to update an existing book                    | Yes              |
|def show_table_data()                                                               | Show a previsualitation of the data base          | Yes              |
|update_book()                                                                       | Update fields in database                         | Yes              |
|def main()                                                                          | Main function to run the workflow                 | Yes              |
|delete_using_db()                                                                   | Delete a book from the database                   | Yes              |
|check_isbn()                                                                        | Check if isbn format is correct                   | Yes              |
|check_string()                                                                      | Check if format is correct when string input      | Yes              |
|check_integer()                                                                     | Check if format is correct when integer input     | Yes              |
|check_format()                                                                      | Check if format format is correct                 | Yes              |
|check_date()                                                                        | Check if date format is correct                   | Yes              |
|check_rate()                                                                        | Check if rate format is correct                   | Yes              |

# Funcionalities

| Navegator                             | Sub-taks 1                     | Sub-task 2                   | Implemented? |
|---------------------------------------|--------------------------------|------------------------------|--------------|
| 1. Añadir un libro                    | 1. Buscar por ISBN             |                              | Yes          |
|                                       | 2. Buscar por título           | 1. Elegir libro a añadir     | Yes          |
|                                       | 3. Buscar por autor            |                              | Yes          |
| 2. Eliminar un libro                  | 1. Seleccionar desde la BD     |                              | Yes          |
| 3. Actualizar un libro                | 1. Seleccionar desde la BD     | 1. Elegir campo a actualizar | Yes          |
| 4. Manejar libros en la base de datos | 1. Previsualizar               |                              | Yes          |
|                                       | 2. Descargar archivo           | 1. csv                       | Yes          |
|                                       |                                | 2. txt                       | Yes          |
|                                       |                                | 3. json                      | Yes          |


# Improvements
- [ ] Redefinir el tipo de las columnas para la base de datos
- [ ] Asegurarse de que en todo momento se mantiene la lógica del tipo de la columna, incluso cuando los datos vienen de la API
- [ ] Cambiar el idioma a español para todo el programa
- [ ] Definir mejor las funciones de manera que el main quede lo más limpio posible.
- [ ] Tanto para las funciones como el main, revisar cómo esta hecho para ir a la pregunta antrior en vez de cerrar el programa.
- [ ] Reemplazar o implementar cuando sea necesario las funciones de los errores.
- [ ] Ver alguna manera para que el usuario pueda seleccionar el idioma de la aplicación al inicio y, en función del idioma, mostrar el lenguaje en una modalidad u otra.
- [ ] Revisar el problema que hay con la función que trae los libros de la API usando el campo autores.
