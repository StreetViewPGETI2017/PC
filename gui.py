from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen
import icons_rc

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
                style = open('style.css','r')
                Dialog.setStyleSheet(style.read())

                frame = self.setUpFrame(Dialog, "frame", (10, 20, 471, 301))
                frame_2 = self.setUpFrame(Dialog, "frame_2", (500, 20, 231, 211))

                up = self.setUpButton(frame, "up", (170, 20, 121, 121))
                down = self.setUpButton(frame, "down", (170, 160, 121, 121))
                left = self.setUpButton(frame, "left", (40, 90, 121, 121))
                right = self.setUpButton(frame, "right", (300, 100, 121, 121))
                camera = self.setUpButton(frame_2, "camera", (20, 30, 191, 151), (130,128))

                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)

                camera.setPalette(palette)
                camera.setCheckable(False)
                camera.setAutoRepeat(False)
                camera.setAutoExclusive(False)

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


        def setUpFrame(self, Dialog, name, geometry):
            frame = QtWidgets.QFrame(Dialog)
            frame.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            frame.setAutoFillBackground(False)
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName(name)
            return frame

        def setUpButton(self, frame, name, geometry, size = (100,100)):
            button = QtWidgets.QPushButton(frame)
            button.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/images/"+name+".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(size[0], size[1]))
            button.setObjectName(name)

            return button




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

