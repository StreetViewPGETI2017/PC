from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen, urlretrieve
import sys, time, os
import subprocess
from urllib.error import HTTPError, URLError
from panorma import stitch

# pobranie ikon
import icons_rc



class Ui_Dialog(object):
        # adres serwera
        __STATIC_ADDRESS = "http://127.0.0.1:5000"  # tu trzeba zmienic

        def __init__(self):
            self.ilosc_zdjec = 8
            self.numer_punktu = 1


        def ilosc_zdjec_f(self):
            ilosc = self.ilosc_zdjec
            return ilosc
        def ping(self, command):
                try:
                        html = urlopen(self.__STATIC_ADDRESS + command, timeout = 1)#trzeba potestowac jaki timeout bedzie ok
                        print(self.__STATIC_ADDRESS + command)
                        return html
                except (HTTPError, URLError)  as error:
                    print (error)
                except:
                    print("duzy error")
        #######################do pingu##################################
        # wysyłanie pingu na serwer

        # jazda prosto
        def runup(self):
                self.ping("/forward")

        # jazda do tyłu
        def rundown(self):
                self.ping("/backward")

        # jazda w lewo
        def runleft(self):
                self.ping("/left")

        # jazda w prawo
        def runright(self):
                self.ping("/right")

        # jazda automatyczna
        def autoMove(self):
                self.ping("/auto")

        # koniec jazdy automatycznej
        def autoStop(self):
                self.ping("/stopauto")

        # podglad zdjecia po sklejaniu, uruchomienie nowego skryptu odpowiedzialnego za wyswietlenie
        def viewPhoto(self):
                subprocess.Popen("view.py 1", shell=True)
        # test
        def viewStreetGUI(self):
                print('test')
                # subprocess.Popen("streetViewGui.py 1", shell=True)

        # uruchomienie kamerki, zczytywanie zdjec
        def runcamera(self):

            # zczytywanie zdjec
            for i in range(0,self.ilosc_zdjec+1,1):
            #path = os.path.abspath("E:/photos/photo" + str(number) + ".jpg") nie mam pendrive pod reka
                time.sleep(1)
                # print(self.__STATIC_ADDRESS + "/static/photo" + str(i))
                # print("E:/photos/photo" + str(i) + ".jpg")

                # czytamy zdjecia o nazwie photo1,photo2 .... photo15 - do ewentualnej zmiany
                # zapis do folderu img - do zmiany na sciezke dysku zewn.
                urlretrieve(self.__STATIC_ADDRESS + "/static/" + str(i) + ".jpg", "img/" + str(i) + ".jpg" ) #<-path
            # po wczytaniu zdjec sklejamy
            time.sleep(1)
            stitch(self.ilosc_zdjec,self.numer_punktu)
            self.numer_punktu=self.numer_punktu+1
            # wyswietlamy wynik (to samo co ViewPhoto)
            subprocess.Popen("view.py", shell=True)



        ######################################################################
        # tworzenie okna GUI
        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                # rozmiar okna
                Dialog.resize(550, 492)
                # style okna CSS
                style = open('style.css','r')
                Dialog.setStyleSheet(style.read())

                # tworzenie ramek na przyciski
                frame = self.setUpFrame(Dialog, "frame", (10, 10, 241, 461))
                frame_2 = self.setUpFrame(Dialog, "frame_2", (270, 10, 261, 271))
                frame_3 = self.setUpFrame(Dialog, "frame_3", (270, 290, 261, 181))

                # przyciski sterujące robotem oraz kamerą
                up = self.setUpButton(frame, "up", (80, 20, 81, 71))
                down = self.setUpButton(frame, "down", (80, 150, 81, 71))
                left = self.setUpButton(frame, "left", (10, 80, 81, 81))
                right = self.setUpButton(frame, "right", (150, 80, 81, 71))
                camera = self.setUpButton(frame_2, "camera", (30, 20, 191, 151), (130,128))
                self.auto_2 = QtWidgets.QPushButton(frame)
                self.auto_2.setGeometry(QtCore.QRect(30, 260, 181, 61))
                self.auto_2.setObjectName("auto_2")
                self.stop = QtWidgets.QPushButton(frame)
                self.stop.setGeometry(QtCore.QRect(30, 360, 181, 61))
                self.stop.setObjectName("stop")

                # Przyciski od zewnetrznych skryptow
                self.viewPhotos = QtWidgets.QPushButton(frame_2)
                self.viewPhotos.setGeometry(QtCore.QRect(20, 180, 221, 61))
                self.viewPhotos.setObjectName("viewPhotos")
                self.streetV = QtWidgets.QPushButton(frame_3)
                self.streetV.setGeometry(QtCore.QRect(30, 30, 211, 111))
                self.streetV.setObjectName("streetV")

                ############################EVENT##############################################################################
                # laczenie przyciskow z akcja

                self.auto_2.clicked.connect(self.autoMove)
                self.viewPhotos.clicked.connect(self.viewPhoto)
                self.streetV.clicked.connect(self.viewStreetGUI)
                self.stop.clicked.connect(self.autoStop)
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
                # nadanie przyciskom tekst
                Dialog.setWindowTitle(_translate("Dialog", "StreetView"))
                self.auto_2.setText(_translate("Dialog", "AUTO"))
                self.viewPhotos.setText(_translate("Dialog", "VIEW"))
                self.streetV.setText(_translate("Dialog", "StreetView"))
                self.stop.setText(_translate("Dialog", "STOP"))



        def setUpFrame(self, Dialog, name, geometry):
            frame = QtWidgets.QFrame(Dialog)
            frame.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            frame.setAutoFillBackground(False)
            frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)
            frame.setObjectName(name)
            return frame

        # tworzenie przyciskow w ktorych nie jest potrzebny tekst
        def setUpButton(self, frame, name, geometry, size = (60,60)):
            button = QtWidgets.QPushButton(frame)
            button.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))
            icon = QtGui.QIcon()
            # dodanie ikony do przycisku
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