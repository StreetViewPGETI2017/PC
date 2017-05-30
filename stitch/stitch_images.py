import numpy as np
import cv2 #pakiet opencv-python, opencv-contrib-python

class stitchImages():
# proste sklejanie, przycina zdjęcia z obu stron, a potem skleja
    def stitch(self,ilosc_zdjec,number_resoult):

        ile = (360 / (ilosc_zdjec + 1))/ 54
        lewy = (1 - ile)/ 2
        prawy = 1 - lewy
        #wczytywanie zdjęć
        images=[]
        for i in range(0,ilosc_zdjec+1):
            image = cv2.imread("../images/"+str(i)+".jpg")
            if image is None:
                print('brak zdjec - sklejanie jest niemozliwe')
                return
            else:
                images.append(image)
        #przycinanie zdjęć
        for i in range(0,ilosc_zdjec + 1):
            try:
                #images[i] = images[i][:, int(0.1296296296 * images[i].shape[1]):int(0.8703703704 * images[i].shape[1])]
                images[i] = images[i][:, int(lewy * images[i].shape[1]):int(prawy * images[i].shape[1])]
            except Exception as err:
                print(err)
        #złożenie dwóch pierwszych zdjęć
        result = np.concatenate((images[0], images[1]), axis=1)
        #składanie reszty zdjęć
        for i in range(1,ilosc_zdjec):
            try:
                result = np.concatenate((result, images[i+1]), axis=1)

            except Exception as err:
                print(err)
        # stworzenie czarnego paska
        x = result.shape[1]
        y = (x - result.shape[0])/4
        blackIm = self.create_blank(x,y)
        # dostawienie czarnego paska na dole i u góry złożeonej panoramy
        result = np.concatenate((result, blackIm), axis=0)
        result = np.concatenate((blackIm, result), axis=0)
        # przeskalowanie
        result = cv2.resize(result,(3432,1732), interpolation = cv2.INTER_CUBIC)
        # zapis
        cv2.imwrite("../streetViewProd/static_assets/result"+str(number_resoult)+".jpg", result)
        cv2.imwrite("result_last.jpg", result)
        print("Sklejono: "+str(number_resoult))
        # cv2.showImage(result)
# tworzenie czarnego obrazu o zadanych wymiarach
    def create_blank(self, width, height, rgb_color=(0, 0, 0)):
        image = np.zeros((int(height), int(width), 3), np.uint8)
        color = tuple(reversed(rgb_color))
        image[:] = color
        return image
#
    def detect(self, image):
        # wykrywanie punktów charakterystycznych i funkcji lokalnych na obrazie(local features)
        descriptor = cv2.xfeatures2d.SIFT_create()
        (k, features) = descriptor.detectAndCompute(image, None)

        k = np.float32([kp.pt for kp in k])

        return k, features

    def match(self, kpA, kpB, featureA, featureB, ratio, reproj):
        # dopasowanie dwóch wektrorów algorytmem k-NN
        matcher = cv2.BFMatcher()
        rawmatches = matcher.knnMatch(featureA, featureB, k=2)
        matches = []
        # odsianie złych dopasowań
        for m in rawmatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # wygenerowanie homografi(homography), trza najmniej 4 dopasowań
        if len(matches) > 4:
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
# awaryjne sklejanie jakby się po punktach nie połączyło
    def emergencyStitching(self, images):
        image2, image1 = images  # w liście zdjęcia od lewej do prawej
        result = np.concatenate((image2, image1), axis=1)
        return result
#funkcja do przycinania zdjęć
    def cut(self, image, lewa, prawa):
        result = image[:, int(lewa * image.shape[1]):int(prawa * image.shape[1])]
        return result

    def uberStitching(self, ilosc_zdjec, number_resoult):
        # sprawdzanie czy jest dość zdjęć by je łączyć po punktach charakterystycznych
        if ilosc_zdjec + 1 < 16:
            self.stitch(ilosc_zdjec, number_resoult)
            return
        else:
            images = []
            liczba = int(ilosc_zdjec + 1)/2
            ile = (360 / liczba) / 54
            lewy = ((1 - ile) / 2)
            prawy = 1 - lewy * 6
            liczbap = ilosc_zdjec + 1
            ilep = (360 / liczbap)/54
            lewyp = ( (1 - ilep) / 2)
            prawyp = 1 - lewyp
            # wczytywanie
            for i in range(0, ilosc_zdjec + 1):
                image = cv2.imread("../images/" + str(i) + ".jpg")
                if image is None:
                    print('brak zdjec - sklejanie jest niemozliwe')
                    return
                else:
                    # zmniejszenie zdjęć i dodanie do listy
                    image = cv2.resize(image, ((int)(0.7 * image.shape[1]), (int)(0.7 * image.shape[0])), interpolation=cv2.INTER_CUBIC)
                    images.append(image)
            # łączenie po 2 zdjęcia w jedno( jak się da to po punktach wspólnych)
            zlaczone = []
            for i in range((int)((ilosc_zdjec + 1) / 2)):
                obrazki = (images[2 * i], images[2 * i + 1])
                try:
                    obrazek = self.stitching(obrazki)
                    obrazek = self.cut(obrazek, lewy, prawy)
                except Exception as eee:
                    obrazki1 = self.cut(obrazki[0], lewyp, prawyp)
                    obrazki2 = self.cut(obrazki[1], lewyp, prawyp)
                    obrazek = self.emergencyStitching((obrazki1, obrazki2))
                if obrazek is None:
                    obrazki1 = self.cut(obrazki[0], lewyp, prawyp)
                    obrazki2 = self.cut(obrazki[1], lewyp, prawyp)
                    obrazek = self.emergencyStitching((obrazki1, obrazki2))
                zlaczone.append(obrazek)
            # składanie
            result = np.concatenate((zlaczone[0], zlaczone[1]), axis=1)

            for i in range(1, int(liczba) - 1):
                result = np.concatenate((result, zlaczone[i + 1]), axis=1)
            # czarny pasek
            x = result.shape[1]
            y = (x - result.shape[0]) / 4

            blackIm = self.create_blank(x, y)

            result = np.concatenate((result, blackIm), axis=0)
            result = np.concatenate((blackIm, result), axis=0)
            # zapis
            result = cv2.resize(result, (3432, 1732), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("../streetViewProd/static_assets/result" + str(number_resoult) + ".jpg", result)
            cv2.imwrite("result_last.jpg", result)
            print("sklejono")


# sklejacz = stitchImages()
# sklejacz.uberStitching(15,5)
# sklejacz.stitch(15,6)