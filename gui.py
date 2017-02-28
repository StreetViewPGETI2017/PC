from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen

class Ui_Dialog(object):
        __STATIC_ADDRESS = "http://127.0.0.1:5000"  # tu trzeba zmienic

        def ping(self, command):
                try:
                        html = urlopen(self.__STATIC_ADDRESS + command)
                        print(self.__STATIC_ADDRESS + command)
                except Exception as err:
                        print("error" + err)

                        # return html.read()
        ##########################keyPressEvent###############################
        # def keyPressEvent(self, e):
        #         if e.key() == Qt.Key_Escape:
        #                 self.close()
        #         if e.key() == Qt.Key_W:
        #                 print("W")
        #                 self.ping("forward")
        #         if e.key() == Qt.Key_S:
        #                 print("S")
        #                 self.ping("backward")
        #         if e.key() == Qt.Key_A:
        #                 print("A")
        #                 self.ping("left")
        #         if e.key() == Qt.Key_D:
        #                 print("D")
        #                 self.ping("right")
        #         if e.key() == Qt.Key_Space:
        #                 print("Space")
        #                 self.ping("camera")
        #######################do pingu##################################3
        def runup(self):
                self.ping("/forward")
        def rundown(self):
                self.ping("/backward")
        def runleft(self):
                self.ping("/left")
        def runright(self):
                self.ping("/right")
        def runcamera(self):
                self.ping("/camera")
        ######################################################################

        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                Dialog.resize(757, 350)
                Dialog.setStyleSheet("QDialog{\n"
        "    background: #616263;\n"
        "}\n"
        "\n"
        "QPushButton{\n"
        "    border:none;\n"
        "    background-color:transparent;\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background: #727374;\n"
        "    border-radius: 10px;\n"
        "}\n"
        "\n"
        "QFrame{\n"
        "        border:10px dotted gray;\n"
        "}\n"
        "QLabel{\n"
        "    border:none;\n"
        "color:white;\n"
        "font-size:15px;\n"
        "}")
                self.frame = QtWidgets.QFrame(Dialog)
                self.frame.setGeometry(QtCore.QRect(10, 20, 471, 301))
                self.frame.setAutoFillBackground(False)
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame")
                self.up = QtWidgets.QPushButton(self.frame)
                self.up.setGeometry(QtCore.QRect(170, 20, 121, 121))
                self.up.setStyleSheet("")
                self.up.setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/images/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.up.setIcon(icon)
                self.up.setIconSize(QtCore.QSize(100, 100))
                self.up.setObjectName("up")
                self.down = QtWidgets.QPushButton(self.frame)
                self.down.setGeometry(QtCore.QRect(170, 160, 121, 121))
                self.down.setStyleSheet("")
                self.down.setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/images/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.down.setIcon(icon1)
                self.down.setIconSize(QtCore.QSize(100, 100))
                self.down.setObjectName("down")
                self.left = QtWidgets.QPushButton(self.frame)
                self.left.setGeometry(QtCore.QRect(40, 90, 121, 121))
                self.left.setText("")
                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap(":/images/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.left.setIcon(icon2)
                self.left.setIconSize(QtCore.QSize(100, 100))
                self.left.setObjectName("left")
                self.right = QtWidgets.QPushButton(self.frame)
                self.right.setGeometry(QtCore.QRect(300, 100, 121, 121))
                self.right.setText("")
                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap(":/images/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.right.setIcon(icon3)
                self.right.setIconSize(QtCore.QSize(100, 100))
                self.right.setObjectName("right")
                self.frame_2 = QtWidgets.QFrame(Dialog)
                self.frame_2.setGeometry(QtCore.QRect(500, 20, 231, 211))
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.camera = QtWidgets.QPushButton(self.frame_2)
                self.camera.setGeometry(QtCore.QRect(20, 30, 191, 151))
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
                self.camera.setPalette(palette)
                self.camera.setStyleSheet("")
                self.camera.setText("")
                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(":/images/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.camera.setIcon(icon4)
                self.camera.setIconSize(QtCore.QSize(130, 128))
                self.camera.setCheckable(False)
                self.camera.setAutoRepeat(False)
                self.camera.setAutoExclusive(False)
                self.camera.setObjectName("camera")

                ############################EVENT##############################################################################
                self.up.clicked.connect(self.runup)
                self.down.clicked.connect(self.rundown)
                self.left.clicked.connect(self.runleft)
                self.right.clicked.connect(self.runright)
                self.camera.clicked.connect(self.runcamera)
                ###############################################################################################################

                self.retranslateUi(Dialog)
                QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "StreetView"))


import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

