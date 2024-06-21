#---------------Программа парсинга входящих в базу данных книг в формате FB2----------------
import xml.etree.ElementTree as ET
import os.path as path
from base64 import decodebytes
from PIL import Image
from io import BytesIO

#---------------Функция переопределения жанра для базы данных---------------
def genre_def(genre_code):
    genres_codes = {"sf_action" : "Научная фантаситка", "prose_rus_classic" : "Российская классика", "literature_19" : "Литература 19-ого века", "literature_17" : "Литература 17-ого века", "literature_18" : "Литература 18-ого века", "humor" : "Комедия"}

    return genres_codes[genre_code]

#---------------Функция конвертирования картинки из формата binary64 в PIL-переменную---------------
def to_picture_convert(binary_data, book_title):
       decoded_picture = decodebytes(binary_data)
       image = BytesIO(decoded_picture)
       pi = Image.open(image)
       
       pi.resize((256, 457))

       box = Image.new("RGB", (pi.size[0],pi.size[1]), (0, 0, 0))
       box.paste(pi)
       box.save(f"Covers/{book_title}.jpg", "JPEG")
#---------------------------------------------------------------------------------------------------

#---------------Функция основного парсинга---------------
def parse_book(book_adress: str):
    #---------------Вход в xml(fb2)-файл---------------
    tree = ET.parse(book_adress)
    root = tree.getroot()
    #--------------------------------------------------

    #-------------!WARNING!-!КРИВОЙ КОД!--Снятие ссылочных тегов для удобства поиска данных--!КРИВОЙ КОД!-!WARNING!--------------
    for elems in root:
        elems.tag = elems.tag.replace("{http://www.gribuser.ru/xml/fictionbook/2.0}", "")
        for subs in elems:
            subs.tag = subs.tag.replace("{http://www.gribuser.ru/xml/fictionbook/2.0}", "")
            for subsubs in subs:
                subsubs.tag = subsubs.tag.replace("{http://www.gribuser.ru/xml/fictionbook/2.0}", "")
                for subsubsubs in subsubs:
                    subsubsubs.tag = subsubsubs.tag.replace("{http://www.gribuser.ru/xml/fictionbook/2.0}", "")
    #-------------------------------------------------------------------------------------------------------                    

    #---------------Отбор первичных характеристик о книге (те которые должы быть в всех книгах)---------------
    book_title = root.find(".description/title-info/book-title").text
    

    if len(root.findall(".description/title-info/author/middle-name")):
        name_author = root.find(".description/title-info/author/first-name").text + " " + root.find(".description/title-info/author/middle-name").text + " " + root.find(".description/title-info/author/last-name").text
    else:
        name_author = root.find(".description/title-info/author/first-name").text + " " + root.find(".description/title-info/author/last-name").text

    genre = genre_def(root.find(".description/title-info/genre").text)

    """genres = []
    for genre in root.findall(".description/title-info/genre"):
        genres.append(genre_def(genre.text))"""
    #----------------------------------------------------------------------------------------------------------

    #---------------Отбор всторостепенных зарактеристик о книге---------------
    try:
        date = root.find(".description/title-info/year").text
    except AttributeError:
        date = "-"
    try:
        annotation = root.find(".description/title-info/annotation/p").text
    except AttributeError:
        annotation = "-"
    try:
        keywords = root.find(".description/title-info/keywords").text
    except AttributeError:
        keywords = "-"
    #-------------------------------------------------------------------------
      
    #---------------Взятие обложки книги---------------
    if (not path.exists(f"Covers/{book_title}.jpg")):
        to_picture_convert((bytes(root.find("binary").text, "utf-8")), book_title)
    #--------------------------------------------------

    return book_title, name_author, genre, date, annotation, keywords

#-------------------------------Функция выдачи текста----------------
def text_give(book_adress: str):
    with open(book_adress, "r+") as f:
        data =  f.read()
        beg = data.index("<body>")
        end = data.index("</body>")
        text = data[beg:end]
        return text
#---------------------------------------------------------------------

#---------------Unit-test---------------
if __name__ == "__main__":
    print(text_give("books/64758176.fb2"))
    
#---------------------------------------books/64758176.fb2