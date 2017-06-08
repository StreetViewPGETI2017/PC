from PyQt5.QtGui import  QFont
from PyQt5.QtCore import  QBasicTimer
from PyQt5.QtWidgets import QLabel, QMainWindow
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

class Map(QMainWindow):
    def __init__(self, __STATIC_ADDRESS,wielkosc_mapy_Param):
            self.__STATIC_ADDRESS = __STATIC_ADDRESS
            self.size = wielkosc_mapy_Param
            self.iconSize = 3
            self.checkedNumber = 0
            self.wallNumber = 0
            self.cameraNumber = 0
            super().__init__()
            self.initUI()

    def initUI(self):

        self.map = ''
        font = QFont()
        font.setPointSize(5)
        self.setStyleSheet("QFrame{\n"
"background:white;\n"
"}\n"
"QPushButton{\n"
"background:red;\n"
"}\n"
"QPushButton#wall{\n"
"background:red;\n"
"}\n"
"QToolButton{\n"
"background:green;\n"
"border:green;\n"
"}\n"
"QLabel{\n"
"background:blue;\n"
"border:blue;\n"
"}\n"
                           )

        self.setGeometry(0, 20, self.size*self.iconSize, self.size*self.iconSize)
        self.setWindowTitle('Mapa')
        self.timer = QBasicTimer()
        self.timer.start(10000, self)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.size*self.iconSize, self.size*self.iconSize)
        self.label.setFont(font)


        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, self.size*self.iconSize, self.size*self.iconSize))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")



        self.paintEventFT()
        for x in range (self.size*5):
            self.wall = QtWidgets.QPushButton(self.frame)
            self.wall.setGeometry(QtCore.QRect(-10, 0, self.iconSize, self.iconSize))
            self.wall.setText("")
            self.wall.setObjectName("wall" + str(self.wallNumber))
            self.wallNumber += 1
        for x in range(int(self.size/2)):
            self.camera = QtWidgets.QLabel(self.frame)
            self.camera.setGeometry(QtCore.QRect(-10, 0, self.iconSize, self.iconSize))
            self.camera.setText("")
            self.camera.setObjectName("camera" + str(self.cameraNumber))
            self.cameraNumber += 1
        for x in range(self.size*5):
            self.checked = QtWidgets.QToolButton(self.frame)
            self.checked.setGeometry(QtCore.QRect(-10 * self.iconSize, 0, self.iconSize, self.iconSize))
            self.checked.setText("")
            self.checked.setObjectName("checked" + str(self.checkedNumber))
            self.checkedNumber += 1


        self.wallNumber = 0
        self.cameraNumber = 0
        self.checkedNumber = 0
        print(self.map)
        for x in range(self.size):
            for y in range(self.size):
                item = self.map[x][y]
                if (item == "1"):
                    objectO = self.findChild(QWidget, "wall" + str(self.wallNumber))
                    objectO.move(y * self.iconSize, x*self.iconSize)
                    self.wallNumber += 1
                if (item == "9"):
                    objectO = self.findChild(QWidget, "camera" + str(self.cameraNumber))
                    objectO.move(y * self.iconSize, x*self.iconSize)
                    self.cameraNumber += 1
                if(item =="2"):
                    objectO = self.findChild(QWidget, "checked" + str(self.checkedNumber))
                    objectO.move(y * self.iconSize, x * self.iconSize)
                    self.checkedNumber += 1


        self.show()

    def timerEvent(self, event):
        self.repaint()



    def paintEvent(self, *args, **kwargs):
        print(self.size)
        changed = False
        try:
            # zmienic na mapa.txt oraz url
            mapa = urlopen(self.__STATIC_ADDRESS + '/static/mapa.txt', timeout=10.0).read().decode()
            open('mapa.txt', 'w').write(mapa)
            changed = True
        except (HTTPError, URLError) as error:
            print(error)
        except Exception as err:
            print(err)
        except:
            print("raspberry nie odpowiada :(")

        with open('mapa.txt') as f:
            map = f.read()  # urlopen(self.__STATIC_ADDRESS + '/static/mapa.txt', timeout=10.0)


        i = 0
        j = 0
        stopped = False

        if(changed==True):
            for item in map:
                if(j==self.size-1):
                    i+=1
                    j=0
                    # print(i)
                    if(i == self.size-1):
                        stopped = True
                        break
                if(self.map[i][j] == "0" and item != "0" and stopped == False):
                    self.board[i][j] = item
                    if (item == "1"):
                        objectO = self.findChild(QWidget, "wall" + str(self.wallNumber))
                        objectO.move(j * self.iconSize, i*self.iconSize)
                        self.wallNumber += 1
                    if (item == "9"):
                        objectO = self.findChild(QWidget, "camera" + str(self.cameraNumber))
                        objectO.move(j * self.iconSize, i*self.iconSize)
                        self.cameraNumber += 1
                    if(item =="2"):
                        objectO = self.findChild(QWidget, "checked" + str(self.checkedNumber))
                        objectO.move(j * self.iconSize, i * self.iconSize)
                        self.checkedNumber += 1

                j+=1
            self.map = self.board

    def paintEventFT(self):
            try:
                map = [
                    [0 for _ in range(self.size-1)] for _ in range(self.size-1)]
            except (HTTPError, URLError)  as error:
                print(error)
                return
            except:
                print("raspberry nie odpowiada :(")
                return
            i = 0
            j = 0
            self.board = []

            for x in range(self.size+1):
                self.board.append(["0"] * self.size)
            for item in map:
                if(j==self.size):
                    i+=1
                    j=0
                self.board[i][j] = item
                j+=1

            #     print mapa
            self.map = self.board
            # for row in self.board:
            #     print(" ".join(row))

            # self.map = map.decode().replace('0', ' ').replace('1', '#')

