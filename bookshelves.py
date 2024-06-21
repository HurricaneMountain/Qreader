#-----------------------------Модуль для виджета ячейки книги------------------------------
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QTextBrowser, QDialog, QScrollArea
from db_works import get_data_from_book
from xml_data_parser import text_give
from db_works import get_book_adress
from book_widg import bookw

#---------------------Класс ячейки, где будет храниться книга------------------
class shelf(QWidget):
    def __init__(self, book_data):
        super().__init__()
        
        self.book_data = book_data
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        self.setFixedSize(440,440)

        self.shelfsort()
        
    def shelfsort(self):
        title, author_name, genre_name, year, annotation, keywords = self.book_data
        book_title = QLabel(text=title, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(book_title)

        hbox = QHBoxLayout()
        cover = QLabel(alignment = Qt.AlignmentFlag.AlignTop)
        cover.setFixedSize(220, 350)
        img = QPixmap(f"Covers/{title}.jpg")
        img = img.scaled(img.width()//3, img.height()//3)
        cover.setScaledContents(1)
        cover.setPixmap(img)
        hbox.addWidget(cover)
        self.main_layout.addLayout(hbox)
        description = QTextBrowser()
        hbox.addWidget(description)

        read_button = QPushButton(text= "Читать книгу!")
        read_button.clicked.connect(self.read)

        self.main_layout.addWidget(read_button)
        #-------------------------Заполнение описания книги---------------------------
        description.setText(f""" Название: {title}\n\nАвтор: {author_name}\n\nЖанр: {genre_name}\n\n   Год: {year}\n\n                   Аннотация:\n{annotation}\n\nКлючевые слова:{keywords}
                            """)
    #---------------------Функция создания окна для чтения------------------------
    def read(self):
        book = QDialog(self)
        book.setWindowTitle(self.book_data[0])
        book.setFixedSize(900, 900)
        book_adress = get_book_adress(self.book_data[0])
        scroll = bookw(book)
        scroll.setGeometry(50, 50, 800, 800)
        scroll.setText(book_adress)
        
        book.exec()
    #------------------------------------------------------------------------------

#------------------------------Unit-test------------------------------------------
def go():
    app = QApplication(sys.argv)

    widget = shelf(get_data_from_book("books/avidreaders.ru__otcy-i-deti.fb2"))
    widget.show()

    app.exec()

if __name__ == "__main__":
    go()
#----------------------------------------------------------------------------