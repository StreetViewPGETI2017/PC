import os
import sys
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, urlretrieve
import yaml
from urllib.parse import urlencode

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

from map import Map
from images import icons_rc
from stitch.stitch_images import stitchImages


class Ui_Dialog():

        def __init__(self):
            # adres serwera
            self.__STATIC_ADDRESS = "http://192.168.137.207:5000"  # tu trzeba zmienic
            self.ilosc_zdjec = 16
            self.numer_punktu = 0
            self.sklejacz = stitchImages()
            #parametry
            self.co_ile_sfera_Param = 500
            self.wielkosc_swiata_Param = 6000
            self.wielkosc_komorki_Param = 100
            self.dostans_od_sciany_Param = 60
            self.wielkosc_mapy_Param = 200

        def ilosc_zdjec_f(self):
            ilosc = self.ilosc_zdjec
            return ilosc

        def ping(self, command):
                try:
                        html = urlopen(self.__STATIC_ADDRESS + command, timeout = 1)#trzeba potestowac jaki timeout bedzie ok
                        print(self.__STATIC_ADDRESS + command)
                        return html.read()
                except (HTTPError, URLError)  as error:
                    print (error)
                    return 0
                except:
                    print("raspberry " + command)
                    return 0
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
                self.ping("/q")

        # jazda w prawo
        def runright(self):
                self.ping("/p")

        # jazda automatyczna
        def autoMove(self):
                threading.Thread(target=self.camera_auto).start()
                # with open('auto_move_configuration.yaml') as file:
                #     config = yaml.load(file)
                #     payload = urlencode(config)
                self.ping("/auto_wall?co_ile_sfera="+str(self.co_ile_sfera_Param)+"&wielkosc_swiata="+str(self.wielkosc_swiata_Param)+"&wielkosc_komorki="+str(self.wielkosc_komorki_Param)+"&dystans_od_sciany="+str(self.dostans_od_sciany_Param) )

        # koniec jazdy automatycznej
        def autoStop(self):
                self.ping("/stopauto")

        def ready(self):
                self.ping("/pcready")

        # podglad zdjecia po sklejaniu, uruchomienie nowego skryptu odpowiedzialnego za wyswietlenie
        def showMap(self):
            try:
                self.map = Map(self.__STATIC_ADDRESS,self.wielkosc_mapy_Param)
            except Exception as err:
                print(err)


        # odpalanie streetView
        def viewStreetGUI(self):
            self.browser = QtWebEngineWidgets.QWebEngineView()
            self.browser.load(QtCore.QUrl.fromLocalFile(os.getcwd()[:-os.getcwd()[::-1].find('\\')] + 'streetViewProd\\index.html'))
            self.browser.show()

        # uruchomienie kamerki, zczytywanie zdjec
        def runcamera(self):

            # zczytywanie zdjec
            for i in range(0, self.ilosc_zdjec, 1):
            #path = os.path.abspath("E:/photos/photo" + str(number) + ".jpg") nie mam pendrive pod reka
                # print(self.__STATIC_ADDRESS + "/static/photo" + str(i))
                # print("E:/photos/photo" + str(i) + ".jpg")

                # czytamy zdjecia o nazwie photo1,photo2 .... photo15 - do ewentualnej zmiany
                # zapis do folderu img - do zmiany na sciezke dysku zewn.
                # edit:17.05 zapisz do folderu images
                try:
                    urlretrieve(self.__STATIC_ADDRESS + "/static/" + str(i) + ".jpg", "../images/" + str(i) + ".jpg" ) #<-path
                except:
                    print('raspberry nie odpowiada' + str(i))
                    return
            # po wczytaniu zdjec skleja
            try:
                self.sklejacz.uberStitching(self.ilosc_zdjec - 1, self.numer_punktu)
            except:
                print("słabe zdjęcia")
                self.sklejacz.stitch(self.ilosc_zdjec - 1, self.numer_punktu)
            try:
                self.ready()
            except:
                print("Nie słyszy!")

            # wyswietlamy wynik (to samo co ViewPhoto)
            # self.view = View()

        def camera_auto(self):
            while True:
                time.sleep(5)
                try:
                    numer_sfery = int(self.ping('/numersfery'))
                except Exception as err:
                    print(err)
                    return
                if numer_sfery == self.numer_punktu + 1:
                    self.numer_punktu = numer_sfery
                    self.runcamera()

        def paramSet(self):
            print("usatwianie parametrow")
            if(len(self.co_ile_sfera.toPlainText())>0):
                self.co_ile_sfera_Param = int(self.co_ile_sfera.toPlainText())
            if (len(self.wielkosc_swiata.toPlainText()) > 0):
                self.wielkosc_swiata_Param = int(self.wielkosc_swiata.toPlainText())
            if (len(self.wielkosc_komorki.toPlainText()) > 0):
                self.wielkosc_komorki_Param = int(self.wielkosc_komorki.toPlainText())
            if (len(self.dostans_od_sciany.toPlainText()) > 0):
                self.dostans_od_sciany_Param = int(self.dostans_od_sciany.toPlainText())
            if (len(self.wielkosc_mapy.toPlainText()) > 0):
                self.wielkosc_mapy_Param = int(self.wielkosc_mapy.toPlainText())
            #print
            # print( self.co_ile_sfera_Param )
            # print( self.wielkosc_swiata_Param )
            # print( self.wielkosc_komorki_Param )
            # print( self.dostans_od_sciany_Param )
            # print( self.wielkosc_mapy_Param )


        ######################################################################
        # tworzenie okna GUI
        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                # rozmiar okna
                Dialog.resize(550, 660)
                # style okna CSS
                style = open('../style/style.css','r')
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
                self.viewMap = QtWidgets.QPushButton(frame_2)
                self.viewMap.setGeometry(QtCore.QRect(20, 180, 221, 61))
                self.viewMap.setObjectName("viewMap")
                self.streetV = QtWidgets.QPushButton(frame_3)
                self.streetV.setGeometry(QtCore.QRect(30, 30, 211, 111))
                self.streetV.setObjectName("streetV")

                #inputy
                self.inputframe = QtWidgets.QFrame(Dialog)
                self.inputframe.setGeometry(QtCore.QRect(0, 470, 540, 180))
                self.inputframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.inputframe.setFrameShadow(QtWidgets.QFrame.Raised)
                self.inputframe.setObjectName("inputframe")
                self.co_ile_sfera = QtWidgets.QTextEdit(self.inputframe)
                self.co_ile_sfera.setGeometry(QtCore.QRect(140, 20, 100, 21))
                self.co_ile_sfera.setObjectName("co_ile_sfera")
                self.label = QtWidgets.QLabel(self.inputframe)
                self.label.setGeometry(QtCore.QRect(10, 20, 100, 21))
                self.label.setObjectName("label")
                self.label_2 = QtWidgets.QLabel(self.inputframe)
                self.label_2.setGeometry(QtCore.QRect(10, 90, 100, 16))
                self.label_2.setObjectName("label_2")
                self.wielkosc_swiata = QtWidgets.QTextEdit(self.inputframe)
                self.wielkosc_swiata.setGeometry(QtCore.QRect(140, 70, 100, 21))
                self.wielkosc_swiata.setObjectName("wielkosc_swiata")
                self.label_3 = QtWidgets.QLabel(self.inputframe)
                self.label_3.setGeometry(QtCore.QRect(280, 20, 130, 16))
                self.label_3.setObjectName("label_3")
                self.wielkosc_komorki = QtWidgets.QTextEdit(self.inputframe)
                self.wielkosc_komorki.setGeometry(QtCore.QRect(430, 20, 100, 21))
                self.wielkosc_komorki.setObjectName("wielkosc_komorki")
                self.label_4 = QtWidgets.QLabel(self.inputframe)
                self.label_4.setGeometry(QtCore.QRect(280, 80, 130, 16))
                self.label_4.setObjectName("label_4")
                self.dostans_od_sciany = QtWidgets.QTextEdit(self.inputframe)
                self.dostans_od_sciany.setGeometry(QtCore.QRect(430, 70, 100, 21))
                self.dostans_od_sciany.setObjectName("dostans_od_sciany")
                self.label_5 = QtWidgets.QLabel(self.inputframe)
                self.label_5.setGeometry(QtCore.QRect(10, 150, 100, 16))
                self.label_5.setObjectName("label_5")
                self.wielkosc_mapy = QtWidgets.QTextEdit(self.inputframe)
                self.wielkosc_mapy.setGeometry(QtCore.QRect(140, 140, 100, 21))
                self.wielkosc_mapy.setObjectName("wielkosc_mapy")

                self.param = QtWidgets.QPushButton(self.inputframe)
                self.param.setGeometry(QtCore.QRect(290, 100, 221, 61))
                self.param.setObjectName("param")

                ############################EVENT##############################################################################
                # laczenie przyciskow z akcja

                self.auto_2.clicked.connect(self.autoMove)
                self.viewMap.clicked.connect(self.showMap)
                self.streetV.clicked.connect(self.viewStreetGUI)
                self.stop.clicked.connect(self.autoStop)
                up.clicked.connect(self.runup)
                down.clicked.connect(self.rundown)
                left.clicked.connect(self.runleft)
                right.clicked.connect(self.runright)
                camera.clicked.connect(self.runcamera)
                self.param.clicked.connect(self.paramSet)
                ###############################################################################################################

                self.retranslateUi(Dialog)
                QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
                _translate = QtCore.QCoreApplication.translate
                # nadanie przyciskom tekst
                Dialog.setWindowTitle(_translate("Dialog", "StreetView"))
                self.auto_2.setText(_translate("Dialog", "AUTO"))
                self.viewMap.setText(_translate("Dialog", "Map"))
                self.streetV.setText(_translate("Dialog", "StreetView"))
                self.stop.setText(_translate("Dialog", "STOP"))
                self.label.setText(_translate("Dialog", "Co ile sfera"))
                self.param.setText(_translate("Dialog", "param"))
                self.label_2.setText(_translate("Dialog", "wielkości świata "))
                self.label_3.setText(_translate("Dialog", "wielkości komórki "))
                self.label_4.setText(_translate("Dialog", "dystans_od_sciany"))
                self.label_5.setText(_translate("Dialog", "wielkosc mapy"))



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
