#-----------------Модуль UI приложения-------------------------------------------------
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout,QVBoxLayout,QPushButton, QLabel, QTextEdit, QComboBox, QFileDialog, QToolBar, QDialog, QStatusBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from booklist import Table
from db_works import get_authors_genres_list, get_filtered_books, add_book_to_db, get_catalog
import options
import os

#--------------------Класс главного меню----------------------------------
class window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setFixedSize(options.WINDOW_WIDTH, options.WINDOW_HEIGHT)
        self.setWindowTitle(options.APP_NAME)

        menu = QToolBar(self)
        self.addToolBar(menu)
        authors_button = QAction("Авторы",self)
        authors_button.triggered.connect(self.authors_win)
        authors_button.setCheckable(1)
        menu.addAction(authors_button)

        self.setStatusBar(QStatusBar(self))

        self.general_layout = QHBoxLayout()
        self.general_layout.setContentsMargins(0,10,10,10)
        self.general_layout.setSpacing(0)
        cent_widget = QWidget()
        cent_widget.setLayout(self.general_layout)

        self.setCentralWidget(cent_widget)
        self.init_ui()

    #------!WARNING!-!КРИВОЙ КОД!------Функция отображения интерфейса главного меню------!WARNING!-!КРИВОЙ КОД!------
    def init_ui(self):
        params_box = QVBoxLayout()
        params_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        params_box.setContentsMargins(0, 20, 0, 100)
        params_box.setSpacing(15)
        self.general_layout.addLayout(params_box)

        params_lab = QLabel(text="Параметры")
        title_lab = QLabel(text="Название книги")

        self.find_book = QTextEdit()
        self.find_book.setFixedSize(QSize(200, 30))

        genre_lab = QLabel(text="Жанр книги")

        self.genre_select = QComboBox()
        self.genre_select.addItem("-")
        self.genre_select.addItems(get_authors_genres_list(0))

        author_lab = QLabel(text="Автор книги")

        self.author_select = QComboBox()
        self.author_select.addItem("-")
        self.author_select.addItems(get_authors_genres_list(1))

        year_lab = QLabel(text="Год выпуска")
        self.year_type = QTextEdit()
        self.year_type.setFixedSize(QSize(200,30))

        self.unequations = QComboBox()
        self.unequations.addItems(["-", "=", "<", ">", "<=", ">=", "!="])

        begin_find = QPushButton(text="Найти")
        begin_find.clicked.connect(self.get_params_info)

        add_book_button = QPushButton(text="Добавить книгу")
        add_book_button.clicked.connect(self.add_book_to_library)

        #----------------Добавление виджетов для параметров в layout для параметров-------
        params_box.addWidget(params_lab, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(title_lab, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(self.find_book, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(genre_lab, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(self.genre_select, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(author_lab, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(self.author_select, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(year_lab, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(self.year_type, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(self.unequations, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(begin_find, alignment=Qt.AlignmentFlag.AlignCenter)
        params_box.addWidget(add_book_button, alignment=Qt.AlignmentFlag.AlignCenter)
        #-----------------------------------------------------------------------------------

        self.library = Table()
        self.library.setFixedSize(900, 1120)
        self.general_layout.addWidget(self.library, alignment=Qt.AlignmentFlag.AlignLeft)
    #------------------------------------------------------------------------------------------------

    #------------------Функция получения свойств фильтрации-----------------------------------------------
    def get_params_info(self):
        #-------------------Заменяем черты на пустые строки---------------------------------------
        book_title = self.find_book.toPlainText()
        if not book_title:
            book_title = ""
        genre_name = self.genre_select.currentText()
        if genre_name == "-":
            genre_name = ""
        author_name = self.author_select.currentText()
        if author_name == "-":
            author_name = ""
        #-----------------------------------------------------------------------------------------
        
        #--------Проверка на отсутсвии значения в поле ввода года-------------------
        try:
            year = int(self.year_type.toPlainText())
        except ValueError:
            year = 0
        #-----------------------------------------------------------------------------

        unequation = self.unequations.currentText()

        #----------------Если пользователь не выбрал разделяющий знак неравенства, но при этом ввёл год, то система поставит за него знак "равно"
        if not year: 
            unequation = ""
        if (unequation == "-") and year:
            unequation = "="
        #--------------------------------------------------------------------------------------------------------------------------

        filtered_catalog = get_filtered_books([book_title, genre_name, author_name, year, unequation])
        self.library.fill_by_books(filtered_catalog)
    #-------------------------------------------------------------------------------------------------

    #-------------Добавление и в директорию библиотеки книги из других директорий-----------------------------
    def add_book_to_library(self):
        home_path = os.getenv("HOME")
        try:
            dir_path = QFileDialog.getOpenFileName(self, caption="Выберите книгу, которую вы хотите добавить", directory= home_path, options=QFileDialog.Option.DontUseNativeDialog)
            file_dir = dir_path[0].split('/')
            file_name= file_dir[len(file_dir) - 1]
            os.replace(dir_path[0], "books/" + file_name)
            add_book_to_db("books/" + file_name)
            self.library.fill_by_books(get_catalog())
        except FileNotFoundError:
            return
    #---------------------------------------------------------------------------------------------------------

    #----------------------Метод вызова окна с именами авторов---------------------------------
    def authors_win(self):
        win = QDialog(self)
        win.setWindowTitle("Авторы")
        win.setFixedSize(170, 150)

        contents = QWidget(win)

        layout = QVBoxLayout(contents)
        layout.setSpacing(20)
        
        authors_lab = QLabel(text="Авторы приложения:")
        layout.addWidget(authors_lab, alignment= Qt.AlignmentFlag.AlignCenter)

        authors = QLabel(text=options.AUTHORS)
        layout.addWidget(authors, alignment= Qt.AlignmentFlag.AlignCenter)

        win.exec()
    #--------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------