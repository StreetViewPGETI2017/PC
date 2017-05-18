import os
import subprocess
import sys
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, urlretrieve
import webbrowser
# from view import View
import numpy as np
import cv2 #pakiet opencv-python, opencv-contrib-python

from images import icons_rc
# from stitch_images import stitch


class stitchImages():#naprawić by można to było wywalić z powrotem do osobnego pliku

    def stitch(self,ilosc_zdjec,number_resoult):

        ile = (360 / (ilosc_zdjec + 1))/ 54
        lewy = (1 - ile)/ 2
        prawy = 1 - lewy

        images=[]
        for i in range(0,ilosc_zdjec+1):
            image = cv2.imread("../img/"+str(i)+".jpg")
            if image is None:
                print('brak zdjec - sklejanie jest niemozliwe')
                return
            else:
                images.append(image)

        for i in range(0,ilosc_zdjec-1):
            try:
                #images[i] = images[i][:, int(0.1296296296 * images[i].shape[1]):int(0.8703703704 * images[i].shape[1])]
                images[i] = images[i][:, int(lewy * images[i].shape[1]):int(prawy * images[i].shape[1])]
            except Exception as err:
                print(err)

        result = np.concatenate((images[0], images[1]), axis=1)

        for i in range(1,ilosc_zdjec):
            try:
                result = np.concatenate((result, images[i+1]), axis=1)

            except Exception as err:
                print(err)

        x = result.shape[1]
        y = (x - result.shape[0])/4

        blackIm = self.create_blank(x,y)

        result = np.concatenate((result, blackIm), axis=0)
        result = np.concatenate((blackIm, result), axis=0)
        result = cv2.resize(result,(3432,1732), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite("../streetViewProd/static_assets/result"+str(number_resoult)+".jpg", result)
        cv2.imwrite("result_last.jpg", result)
        print("Sklejono: "+str(number_resoult))
        # cv2.showImage(result)

    def create_blank(self, width, height, rgb_color=(0, 0, 0)):
        image = np.zeros((int(height), int(width), 3), np.uint8)
        color = tuple(reversed(rgb_color))
        image[:] = color
        return image

    def detect(self, image):
        # wykrywanie punktów charakterystycznych
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()
        (k, features) = descriptor.detectAndCompute(image, None)

        k = np.float32([kp.pt for kp in k])

        return k, features

    def match(self, kpA, kpB, featureA, featureB, ratio, reproj):
        matcher = cv2.BFMatcher()
        rawmatches = matcher.knnMatch(featureA, featureB, k=2)
        matches = []

        for m in rawmatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 2:
            ptsA = np.float32([kpA[i] for (_, i) in matches])
            ptsB = np.float32([kpB[i] for (i, _) in matches])

            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reproj)

            return matches, H, status

        return None

    def stitching(self, images):
        image2, image1 = images  # w liście zdjęcia od lewej do prawej
        kp1, features1 = self.detect(image1)
        kp2, features2 = self.detect(image2)

        M = self.match(kp1, kp2, features1, features2, 0.75, 4.0)
        if M == None:
            return None

        matches, H, status = M
        result = cv2.warpPerspective(image1, H, (image1.shape[1] + image2.shape[1], image1.shape[0]))
        result[0:image2.shape[0], 0:image2.shape[1]] = image2
        return result

    def uberStitching(self, ilosc_zdjec, number_resoult):
        if ilosc_zdjec + 1 < 16:
            self.stitch(ilosc_zdjec, number_resoult)
            return
        else:
            images = []
            for i in range(0, ilosc_zdjec + 1):
                image = cv2.imread("../img/" + str(i) + ".jpg")
                if image is None:
                    print('brak zdjec - sklejanie jest niemozliwe')
                    return
                else:
                    images.append(image)
            zlaczone = []
            for i in range((int)((ilosc_zdjec + 1) / 2)):
                obrazki = (images[2 * i], images[2 * i + 1])
                obrazek = self.stitching(obrazki)
                zlaczone.append(obrazek)

            liczba = len(zlaczone)
            ile = (360 / liczba) / 54
            lewy = (1 - ile) / 2
            prawy = 1 - lewy * 6

            for i in range(0, liczba + 1):
                try:
                    zlaczone[i] = zlaczone[i][:, int(lewy * zlaczone[i].shape[1]):int(prawy * zlaczone[i].shape[1])]
                except Exception as err:
                    print(err)

            result = np.concatenate((zlaczone[0], zlaczone[1]), axis=1)

            for i in range(1, liczba - 1):
                result = np.concatenate((result, zlaczone[i + 1]), axis=1)

            x = result.shape[1]
            y = (x - result.shape[0]) / 4

            blackIm = self.create_blank(x, y)

            result = np.concatenate((result, blackIm), axis=0)
            result = np.concatenate((blackIm, result), axis=0)

            result = cv2.resize(result, (3432, 1732), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("../streetViewProd/static_assets/result" + str(number_resoult) + ".jpg", result)
            cv2.imwrite("result_last.jpg", result)
            print("ok")


class Ui_Dialog():

        def __init__(self):
            # adres serwera
            self.__STATIC_ADDRESS = "http://127.0.0.1:5000"  # tu trzeba zmienic
            self.ilosc_zdjec = 16
            self.numer_punktu = 0
            self.sklejacz = stitchImages()

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
                    print("raspberry nie odpowiada :(")
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
                self.ping("/left")

        # jazda w prawo
        def runright(self):
                self.ping("/right")

        # jazda automatyczna
        def autoMove(self):
                threading.Thread(target=self.camera_auto).start()
                self.ping("/auto")

        # koniec jazdy automatycznej
        def autoStop(self):
                self.ping("/stopauto")

        def ready(self):
                self.ping("/pcready")

        # podglad zdjecia po sklejaniu, uruchomienie nowego skryptu odpowiedzialnego za wyswietlenie
        def viewPhoto(self):
            # self.view = View()
            self.browser = QtWebEngineWidgets.QWebEngineView()
            self.browser.load(
                QtCore.QUrl.fromLocalFile(os.getcwd()[:-os.getcwd()[::-1].find('\\')] + 'streetViewProd\\index.html'))
            self.browser.show()

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
                    urlretrieve(self.__STATIC_ADDRESS + "/static/" + str(i) + ".jpg", "images/" + str(i) + ".jpg" ) #<-path
                except:
                    print('raspberry nie odpowiada' + str(i))
                    #return
            # po wczytaniu zdjec sklejamy
            self.numer_punktu = self.numer_punktu + 1

            self.sklejacz.uberStitching(self.ilosc_zdjec - 1, self.numer_punktu)
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
                    continue
                if numer_sfery != self.numer_punktu:
                    self.runcamera()


        ######################################################################
        # tworzenie okna GUI
        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                # rozmiar okna
                Dialog.resize(550, 492)
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