import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QBasicTimer, QRect
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QMainWindow, QPushButton
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

class Map(QMainWindow):
    def __init__(self, __STATIC_ADDRESS):
            self.__STATIC_ADDRESS = __STATIC_ADDRESS
            super().__init__()
            self.initUI()

    def initUI(self):
        self.map = ''
        font = QFont()
        font.setPointSize(5)
        self.setGeometry(50, 50, 600, 600)
        self.setWindowTitle('Mapa')
        self.timer = QBasicTimer()
        self.timer.start(10, self)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 600, 600)
        self.label.setFont(font)
        self.show()

    def timerEvent(self, event):
        self.repaint()

    def paintEvent(self, *args, **kwargs):
        try:
            map = urlopen(self.__STATIC_ADDRESS + '/static/mapa.txt', timeout=10.0)
            map = map.read()  # trzeba potestowac jaki timeout bedzie ok
        except (HTTPError, URLError)  as error:
            print(error)
            return
        except:
            print("raspberry nie odpowiada :(")
            return
        self.map = map.decode()
        self.label.setText(self.map)
