# Description
Keep track of the books you've read, store general information such as ISBN, title, description, etc., and add individual information like your own rating, reading date, etc. Have all the information about your books collected in one place.

# Fields

|Column         | Origin     |  Path API                             | Type    |
|---------------|------------|---------------------------------------|---------|
|isbn           | Input, API |                                       | INT     |
|title          | Input, API |                                       | STRING  |
|authors        | Input, API |                                       | STRING  |
|description    | API        | items.description                     | STRING  |
|published_date | API        |                                       | DATE    |
|page_count     | API        | items.volumeInfo.pageCount            | INT     |
|formate        | Input      |                                       | STRING  |
|languaje       | API        | items.volumeInfo.language             | STRING  |
|genders        | API        | items.volumeInfo.categories           | STRING  |
|image_links    | API        | items.volumeInfo.imageLinks.thumbnail | STRING  |
|preview_link   | API        | items.volumeInfo.previewLink          | STRING  |
|read_date      | Input      |                                       | DATE    |
|rate           | Input      |                                       | INT     |
|times_readed   | Input      |                                       | INT     |


# Functions

| Command                                                                            | Description                                      | In main script ? |
|------------------------------------------------------------------------------------|--------------------------------------------------|------------------|
|def setup_database(db_name='personal.db')                                           | Set up the SQLite database                       | Yes              |
|def fetch_book_data_isbn(isbn)                                                      | Fetch book data from Google Books API using ISBN | No               |
|def fetch_book_data_title(title)                                                    | Fetch book data from Google Books API using Ttile| Yes              |
|def get_read_date()                                                                 | Get read_date information                        | Yes              |
|def get_rate()                                                                      | Get rate information                             | Yes              |
|def get_times_readed()                                                              | Get times readed                                 | Yes              |
|def get_book_format()                                                               | Get book format                                  | Yes              |
|save_book_to_db(book, read_date, rate, times_readed, formato, db_name='personal.db')| Save book data to database                       | Yes              |
|book_exists(isbn, db_name='personal.db')                                            | Check if the book already exists in the database | Yes              |
|def ask_updates(isbn, db_name='personal.db')                                        | Ask to update an existing book                   | Yes              |
|def main()                                                                          | Main function to run the workflow                | Yes              |



# Funcionalities

| Navegator                             | Sub-taks 1                     | Sub-task 2                   | Implemented? |
|---------------------------------------|--------------------------------|------------------------------|--------------|
| 1. Añadir un libro                    | 1. Buscar por ISBN             |                              | Yes          |
|                                       | 2. Buscar por título           | 1. Elegir libro a añadir     | Yes          |
|                                       | 3. Buscar por autor            |                              | No           |
| 2. Eliminar un libro                  | 1. Buscar por ISBN             |                              | No           |
|                                       | 2. Buscar por título           |                              | No           |
|                                       | 3. Buscar por autor            |                              | No           |
|                                       | 4. Buscar en la base de datos  |                              | No           |
| 3. Actualizar un libro                | 1. Buscar por ISBN             | 1. Elegir campo a actualizar | No           |
|                                       | 2. Buscar por título           | 1. Elegir campo a actualizar | No           |
|                                       | 3. Buscar por autor            | 1. Elegir campo a actualizar | No           |
|                                       | 4. Buscar en la base de datos  | 1. Elegir campo a actualizar | No           |
| 3. Mostrar libros en la base de datos |                                |                              | No           |