from urllib.request import urlopen
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

class GUI(QWidget):

    __STATIC_ADDRESS = "http://192.168.43.37:5000/"#tu trzeba zmienic

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('StreetView')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_W:
            print("W")
            self.ping("forward")
        if e.key() == Qt.Key_S:
            print("S")
            self.ping("backward")
        if e.key() == Qt.Key_A:
            print("A")
            self.ping("left")
        if e.key() == Qt.Key_D:
            print("D")
            self.ping("right")
        if e.key() == Qt.Key_Space:
            print("Space")
            self.ping("camera")

    def ping(self, command):
        try:
            html = urlopen(self.__STATIC_ADDRESS + command)
        except Exception as err:
            print(err)

        #return html.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())