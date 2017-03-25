from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen, urlretrieve
import sys, time, os
import icons_rc
import subprocess
from urllib.error import HTTPError, URLError

class Ui_Dialog(object):
        __STATIC_ADDRESS = "http://127.0.0.1:5000"  # tu trzeba zmienic

        def ping(self, command):
                try:
                        html = urlopen(self.__STATIC_ADDRESS + command, timeout = 1)
                        print(self.__STATIC_ADDRESS + command)
                        return html
                except (HTTPError, URLError)  as error:
                    print (error)
                except:
                    print("duzy error")
        #######################do pingu##################################
        def runup(self):
                self.ping("/forward")
        def rundown(self):
                self.ping("/backwards")
        def runleft(self):
                self.ping("/left")
        def runright(self):
                self.ping("/right")
        def autoMove(self):
                self.ping("/auto")
        def viewPhoto(self):
                print('test')
                subprocess.Popen("view.py 1", shell=True)
        def runcamera(self):
                time.sleep(1)
                number = 1
                #path = os.path.abspath("E:/photos/photo" + str(number) + ".jpg") nie mam pendrive pod reka
                urlretrieve(self.__STATIC_ADDRESS + "/static/test.jpg", "photo.jpg" ) #<-path


        ######################################################################

        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                Dialog.resize(550, 371)
                style = open('style.css','r')
                Dialog.setStyleSheet(style.read())

                frame = self.setUpFrame(Dialog, "frame", (10, 10, 241, 341))
                frame_2 = self.setUpFrame(Dialog, "frame_2", (270, 10, 261, 341))

                up = self.setUpButton(frame, "up", (80, 20, 81, 71))
                down = self.setUpButton(frame, "down", (80, 150, 81, 71))
                left = self.setUpButton(frame, "left", (10, 80, 81, 81))
                right = self.setUpButton(frame, "right", (150, 80, 81, 71))
                camera = self.setUpButton(frame_2, "camera", (40, 40, 191, 151), (130,128))

                self.auto_2 = QtWidgets.QPushButton(frame)
                self.auto_2.setGeometry(QtCore.QRect(30, 240, 181, 61))
                self.auto_2.setObjectName("auto_2")
                self.viewPhotos = QtWidgets.QPushButton(frame_2)
                self.viewPhotos.setGeometry(QtCore.QRect(20, 240, 221, 61))
                self.viewPhotos.setObjectName("viewPhotos")

                self.auto_2.clicked.connect(self.autoMove)
                self.viewPhotos.clicked.connect(self.viewPhoto)

                ############################EVENT##############################################################################
                up.clicked.connect(self.runup)
                down.clicked.connect(self.rundown)
                left.clicked.connect(self.runleft)
                right.clicked.connect(self.runright)
                camera.clicked.connect(self.runcamera)
                ###############################################################################################################

                self.retranslateUi(Dialog)
                QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "StreetView"))
                self.auto_2.setText(_translate("Dialog", "AUTO"))
                self.viewPhotos.setText(_translate("Dialog", "VIEW"))

        def setUpFrame(self, Dialog, name, geometry):
            frame = QtWidgets.QFrame(Dialog)
            frame.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            frame.setAutoFillBackground(False)
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName(name)
            return frame

        def setUpButton(self, frame, name, geometry, size = (60,60)):
            button = QtWidgets.QPushButton(frame)
            button.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/images/"+name+".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(size[0], size[1]))
            button.setObjectName(name)
            return button

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())