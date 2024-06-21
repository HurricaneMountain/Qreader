#------------Программа для виджета таблицы книг--------------
import sys
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from bookshelves import shelf
from db_works import get_catalog, get_data_from_book

class Table(QtWidgets.QWidget):
    
    def __init__(self):
        super(Table, self).__init__()
        
        self.initUI()
        catalog = get_catalog()
        self.fill_by_books(catalog)

    #----------Создание интерфейса для виджета-----------    
    def initUI(self):
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setFixedSize(900, 1000)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(10)
    #----------------------------------------------------

#-----------Рекурсивная функция по очистке таблицы от старых виджетов при фильтрации----------
    def clear_table(self, layout):
         if self.vbox is not None:
            while self.vbox.count():
                item = self.vbox.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_table(item.layout())
#--------------------------------------------------------------------------------------------

    #----------Функция заполнения таблицы книгами в БД-------------------
    def fill_by_books(self, book_catalog):
        self.clear_table(self.vbox)
        book_count = len(book_catalog)

        if not book_count: 
            return # Таблицу не заполняем
        
        rows_count = round(book_count/2)
        k = 0 #Счётчик для итерации каталога
        flag = 0 #Для прерывания цикла после прохождения всего каталога
                
        if book_count == 1:
            hbox = QtWidgets.QHBoxLayout()
            self.vbox.addLayout(hbox)
            hbox.addWidget(shelf(get_data_from_book(book_catalog[0])))

        else:
            for i in range(rows_count):
                hbox = QtWidgets.QHBoxLayout()
                self.vbox.addLayout(hbox)

                for j in range(2):

                    if k == book_count:
                        flag = 1
                        break

                    book_data = get_data_from_book(book_catalog[k])
                    cur = shelf(book_data)
                    hbox.addWidget(cur, alignment= Qt.AlignmentFlag.AlignCenter)
                    k+=1

                if flag:
                    break

        widget = QtWidgets.QWidget()
        widget.setLayout(self.vbox)
        self.scroll.setWidget(widget)
    #----------------------------------------------------------------------------

def main():
    print(get_catalog())
    app = QtWidgets.QApplication(sys.argv)
    ex = Table()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
