#-------------------Модуль для работы с базами данных SQLite----------------
import sqlite3
from xml_data_parser import parse_book

#------------------Функция по вставке возможно отсутствующих жанра и автора в базу данных-----------
def put_author_and_genre(genre_name, author_name):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    #-----------Если полученный массив пустой, то добавляем жанр или автора в таблицу---------------
    if not cur.execute(f"SELECT author_id FROM authors WHERE author_name = ?", (author_name,)).fetchall():
        cur.execute("INSERT INTO authors (author_name) VALUES (?)", (author_name,))
        con.commit()

    if not cur.execute(f"SELECT genre_id FROM genres WHERE genre_name = ?", (genre_name,)).fetchall():
        cur.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,))
        con.commit()

    cur.close()
    con.close()
#---------------------------------------------------------------------------------------------------

#---------------------Получение ID-шников автора и жанра----------------
def get_author_genre_ids(author_name, genre_name):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    author_id = cur.execute(f"SELECT author_id FROM authors WHERE author_name = ?", (author_name,)).fetchone()[0]
    genre_id = cur.execute(f"SELECT genre_id FROM genres WHERE genre_name = ?", (genre_name,)).fetchone()[0]

    cur.close()
    con.close()

    return author_id, genre_id
#-------------------------------------------------------------------------

#--------------------Добавляем расположение книги в БД для будущей связи с книжными файлами--------------------
def add_adress_in_db(book_name ,book_adress):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    book_id =  cur.execute(f"SELECT book_id FROM bookhub WHERE book_name = ?", (book_name,)).fetchone()[0]
    
    cur.execute("INSERT INTO adresses VALUES (?, ?)", (book_id, book_adress))
    con.commit()

    cur.close()
    con.close()
#----------------------------------------------------------------------------------------------------------------

#--------------------------Функция добавления информации о книге формата FB2 в
                        # основную таблицу БД (работает только при первом добавлении файла при отсутствии её записей в БД)-----------------------
def add_book_to_db(book_adress):

    book_name, author_name, genre_name, year, annotation, keywords = parse_book(book_adress)

    put_author_and_genre(genre_name, author_name)

    author_id, genre_id = get_author_genre_ids(author_name, genre_name)
    
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()
    
    try:
        cur.execute("""INSERT INTO bookhub (book_name, author_id, genre_id, year, annotation, keywords) 
                    VALUES (?, ?, ?, ?, ?, ?)""", (book_name, author_id, genre_id, year, annotation, keywords))
        con.commit()
    except sqlite3.IntegrityError:
        pass

    cur.close()
    con.close()

    add_adress_in_db(book_name, book_adress)
#------------------------------------------------------------------------------------------------------------------------------------------

#------------------Функция получения последнего сохранённого каталога файлов-----------------------------------------
def get_catalog():
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    catalog = cur.execute("SELECT book_adress FROM adresses").fetchall()

    cur.close()
    con.close()
    return [catalog[i][0] for i in range(len(catalog))] 
#--------------------------------------------------------------------------------------------------------------------

#----------------Удаление Книг из библиотеке в случае их отсутствия их в директории------------------
def delete_book_from_db(book_adress):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    book_id = cur.execute(f"SELECT book_id FROM adresses WHERE book_adress = ?", (book_adress,)).fetchone()[0]

    cur.execute(f"DELETE FROM adresses WHERE book_id = ?", (book_id,))
    con.commit()
    cur.execute(f"DELETE FROM bookhub WHERE book_id = ?", (book_id,))
    con.commit()

    cur.close()
    con.close()
#----------------------------------------------------------------------------------------------------

#------------------------Сбор данных о книге по её расположению-------------------------
def get_data_from_book(book_adress):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    book_id = cur.execute(f"SELECT book_id FROM adresses WHERE book_adress = ?", (book_adress,)).fetchone()[0]
    write = cur.execute(f"""SELECT book_name, author_name, genre_name, year, annotation, keywords
                        FROM bookhub JOIN authors ON bookhub.author_id = authors.author_id
                        JOIN genres ON bookhub.genre_id = genres.genre_id
                        WHERE book_id = ? """, (book_id,)).fetchone()
    
    cur.close()
    con.close()
    return write
#------------------------------------------------------------------------------------------

#---------------------Получение списка жанров или авторов------------------------------------
def get_authors_genres_list(is_author: bool):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    if is_author:
        authors_list = cur.execute("SELECT author_name from authors").fetchall()
        cur.close()
        con.close()
        return [authors_list[i][0] for i in range(len(authors_list))]
    else:
        genres_list = cur.execute("SELECT genre_name FROM genres").fetchall()
        cur.close()
        con.close()
        return [genres_list[i][0] for i in range (len(genres_list))]
#--------------------------------------------------------------------------------------------
def get_book_adress(book_name):
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    book_id = cur.execute(f"SELECT book_id from bookhub where book_name = '{book_name}'").fetchone()[0]
    adress = cur.execute(f"SELECT book_adress FROM adresses WHERE book_id = ?", (book_id,)).fetchone()[0]

    return adress

#--------------------Функция получения списка книг согласно фильтрам---------------
def get_filtered_books(parameters):
    book_name, genre_name, author_name, year, unequation = parameters
    con = sqlite3.connect("dbs/bookhub")
    cur = con.cursor()

    if not year:
        filtered_catalog = cur.execute(f"""SELECT book_adress
                                        FROM bookhub b JOIN authors a ON b.author_id = a.author_id
                                        JOIN genres g ON g.genre_id = b.genre_id
                                       JOIN adresses adr ON adr.book_id = b.book_id
                                       WHERE book_name like '{book_name}%' AND genre_name like '{genre_name}%' and author_name like '{author_name}%' """).fetchall()
        
    else:
        filtered_catalog = cur.execute(f"""SELECT book_adress
                                        FROM bookhub b JOIN authors a ON b.author_id = a.author_id
                                        JOIN genres g ON g.genre_id = b.genre_id
                                       JOIN adresses adr ON adr.book_id = b.book_id
                                       WHERE book_name like '{book_name}%' AND genre_name like '{genre_name}%' and author_name like '{author_name}%' AND year {unequation} {year} """).fetchall()

    cur.close()
    con.close()
    return [filtered_catalog[i][0] for i in range(len(filtered_catalog))]

    cur.close()
    con.close()
#----------------------------------------------------------------------------------

#-------------------Unit-test------------
if __name__ == "__main__":
    print(get_filtered_books(["", "", "", 0, ""]))
#----------------------------------------