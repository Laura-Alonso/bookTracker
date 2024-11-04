from utils.check import * 
from utils.get_information import * 
import sqlite3


def save_book_to_db(db_name='personal.db', tabla = "books"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("Book succesfully added")
    read_date = get_read_date()
    rate = get_rate()
    times_readed = get_times_readed()
    formate = get_book_format()

    # Insert book data into the database
    cursor.execute('''
        INSERT OR IGNORE INTO books 
        (isbn, title, authors, description, published_date, page_count, formato, language, genders, preview_link, image_links, read_date, rate, times_readed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tabla['isbn'], tabla['title'], tabla['authors'], tabla['description'], 
        tabla['published_date'],  tabla['page_count'], formate, tabla['language'], tabla['genders'], 
        tabla['preview_link'], tabla['image_links'], read_date, rate, times_readed
    ))
    
    conn.commit()
    conn.close()


save_book_to_db()   