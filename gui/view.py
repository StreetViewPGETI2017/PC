import sys
from PyQt5 import QtGui, QtWidgets


class View(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()


        self.title = 'View'

        # polozenie okienka na okranie
        self.left = 100
        self.top = 100

        # rozmiar okna
        self.width = 1300
        self.height = 500
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QtWidgets.QLabel(self)
        # czytanie zdjecia
        pixmap = QtGui.QPixmap('exl.jpg')
        # zmiana rozmiaru zdjecia do wielkosci okna
        pixmap = pixmap.scaled(self.width,self.height)

        # pixmap = pixmap.scaledToWidth(width)
        # pixmap = pixmap.scaledToHeight(height)

        # dodanie zdjecia do label
        label.setPixmap(pixmap)

        # self.resize(self.width, self.height)

        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = View()
    sys.exit(app.exec_())