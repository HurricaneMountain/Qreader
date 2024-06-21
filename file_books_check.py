import options
import os
from db_works import get_catalog, add_book_to_db, delete_book_from_db

def current_catalog():
    return os.listdir("books/")

def fill_db():
    catalog_old = get_catalog()
    catalog_now = [ "books/" + current_catalog()[i] for i in range(len(current_catalog()))]
    for i in range (len(catalog_now)):
        if catalog_now[i] not in catalog_old:
            add_book_to_db(catalog_now[i])

    for i in range(len(catalog_old)):
        if catalog_old[i] not in catalog_now:
            delete_book_from_db(catalog_old[i])


if __name__ == "__main__":
    fill_db()