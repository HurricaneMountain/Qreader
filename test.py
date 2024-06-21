from PyQt6.QtWidgets import QScrollArea,QWidget, QVBoxLayout, QLabel, QMainWindow, QApplication
import sys 

# class for scrollable label
class ScrollLabel(QScrollArea):
  
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
  
        # making widget resizable
        self.setWidgetResizable(True)
  
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
  
        # vertical box layout
        lay = QVBoxLayout(content)
  
        # creating label
        self.label = QLabel(content)
  
        # making label multi-line
        self.label.setWordWrap(True)
  
        # adding label to the layout
        lay.addWidget(self.label)
  
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
  
    # getting text method
    def text(self):
  
        # getting text of the label
        get_text = self.label.text()
  
        # return the text
        return get_text
  
class Window(QMainWindow):
  
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
  
        # calling method
        self.UiComponents()
  
        # showing all the widgets
        self.show()
  
    # method for widgets
    def UiComponents(self):
        # text to show in label
        text = """There are so many options provided by Python to develop GUI 
               There are so many options provided by Python to develop GUI
               There are so many options provided by Python to develop GUI"""
  
        # creating scroll label
        label = ScrollLabel(self)
  
        # setting text to the label
        label.setText(text)
  
        # setting geometry
        label.setGeometry(100, 100, 150, 80)
  
        # setting tool tip
        label.setToolTip("It is tool tip")
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())