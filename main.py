#---------------Main приложения-----------------
from PyQt6.QtWidgets import QApplication
import sys
from file_books_check import fill_db
from front import window

def main():
    app = QApplication(sys.argv)
    fill_db()
    win = window()

    win.show()

    app.exec()

if __name__ == "__main__":
    main()