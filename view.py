import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import  QPixmap


class App(QWidget):


    def __init__(self):
        super().__init__()


        self.title = 'View'
        self.left = 250
        self.top = 250
        self.width = 640
        self.height = 1480
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)


        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        width = 1300;
        height= 500;
        label = QLabel(self)
        pixmap = QPixmap('exl.jpg')
        pixmap = pixmap.scaled(width,height)
        # pixmap = pixmap.scaledToWidth(width)
        # pixmap = pixmap.scaledToHeight(height)
        label.setPixmap(pixmap)
        self.resize(width, height)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())