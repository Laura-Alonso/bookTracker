from utils.update import * 
from utils.check import * 
from utils.get_information import * 
import sqlite3

# Update book data
def update_book(db = "personal", tabla = "books", row=None, question = None):

    # Create SQL conecction to our SQLite database
    con = sqlite3.connect(f'./{db}.db')

    df = pd.read_sql_query(f"SELECT rowid AS Id, isbn, title, authors, description, published_date, page_count, formato, language, genders, read_date, rate, times_readed FROM {tabla}", con)
    df_truncate = df

    # Fix format to markdown
    truncation_rules = {
        "title": 45,
        "authors": 10,
        "description": 15,
        "genders": 20
    }
    
    for col, max_length in truncation_rules.items():
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x)[:max_length] + '...' if isinstance(x, str) and len(x) > max_length else x)
    
    # Obtenemos los resultados
    print(df_truncate.to_markdown(index=False,  
                         floatfmt=".0f"))

    # Preguntar que libro quiere actualizar
    row = int(input("\nIntroduzca el 'Id' ('idetificador') del libro que quiere actualizar: "))
    campos = {
        "Opción 1": "ISBN",
        "Opción 2": "Título",
        "Opción 3": "Autor/es",
        "Opción 4": "Descripción",
        "Opción 5": "Fecha de publicación",
        "Opción 6": "Número de páginas",
        "Opción 7": "Formato",
        "Opción 8": "Idioma",
        "Opción 9": "Genero/s",
        "Opción 10": "Fecha de lectura",
        "Opción 11": "Puntuación del libro",
        "Opción 12": "Número de veces leido"
    }
    campos_legibles = "\n".join([f"{opcion}: {campo}" for opcion, campo in campos.items()])
    question = int(input(f"\n¿Qué campo quieres actualizar (introduzca un número del 1 al 12?: \n\n{campos_legibles} \n\n"))

    # Isbn
    if question == 1:
        update_book_isbn(row=row)

    # Title
    elif question == 2:
        udpate_book_title(row=row)

    # Author/s
    elif question == 3:
        udpate_book_author(row=row)

    # Description
    elif question == 4:
        udpate_book_description(row=row)
    
    # Publish date
    elif question == 5:
        udpate_book_publish_date(row=row)   

    # Publish date
    elif question == 6:
        udpate_book_page_count(row=row)     

    # Book format
    elif question == 7:
        udpate_book_format(row=row)  

     # Language
    elif question == 8:
        udpate_book_language(row=row)          

    # Gender
    elif question == 9:
        udpate_book_gender(row=row)  

    # Reading date
    elif question == 10:
        udpate_book_reading_date(row=row) 

    # Rate
    elif question == 11:
        udpate_book_rate(row=row) 

    # Times readed
    elif question == 12:
        udpate_book_times_readed(row=row)

    # Others
    else:
        print("\nHa habido un error\n")

# Close conexion with bd
    con.close() 



# Save extra information 
def save_book_to_db(book_data, db_name='personal.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("\nBook succesfully added\n")
    read_date = get_read_date()
    rate = get_rate()
    times_readed = get_times_readed()
    formate = get_book_format()

    cursor.execute('''
        INSERT OR IGNORE INTO books 
        (isbn, title, authors, description, published_date, page_count, formato, language, genders, preview_link, image_links, read_date, rate, times_readed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        book_data['isbn'], book_data['title'], book_data['authors'], book_data['description'], 
        book_data['published_date'],  book_data['page_count'], formate, book_data['language'], book_data['genders'], 
        book_data['preview_link'], book_data['image_links'], read_date, rate, times_readed
    ))
    
    conn.commit()
    conn.close()
    