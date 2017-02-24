from urllib.request import urlopen
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

class GUI(QWidget):

    __STATIC_ADDRESS = "http://www.onet.pl"

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
            print(GUI.ping(self,""))
        if e.key() == Qt.Key_S:
            print("S")
        if e.key() == Qt.Key_A:
            print("A")
        if e.key() == Qt.Key_D:
            print("D")
        if e.key() == Qt.Key_Space:
            print("Space")

    def ping(self, command):
        html = urlopen(self.__STATIC_ADDRESS + command)

        return html.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())