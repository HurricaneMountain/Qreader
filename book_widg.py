#------------------------------Класс виджета прочтения книги------------------------------------------
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from xml_data_parser import text_give
from bs4 import BeautifulSoup

#--------------------------Класс дорожки текста------------------------
class bookw(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
  
        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)
  
        lay = QVBoxLayout(content)
  
        self.label = QLabel(content)
  
        self.label.setWordWrap(True)

        lay.addWidget(self.label)
    #---------------------Устанавливаем текст на дорожку--------------
    def setText(self, book_adress):
        text = text_give(book_adress)
        soup = BeautifulSoup(text)
        text = soup.get_text()
        self.label.setText(text)
    #-------------------------------------------------------------------
#------------------------------------------------------------------------