import numpy as np
import imutils
import cv2

#psuje się przy dołączniu 3 zdjęcia
#wincyj zdjęć


class Stitcher:
    def __init__(self):
        self.isv3 = imutils.is_cv3()
#łączenie 2 zdjęć
    def stitch(self, images):
        image2, image1 = images #w liście zdjęcia od lewej do prawej
        kp1, features1 = self.detect(image1)
        kp2, features2 = self.detect(image2)

        M = self.match(kp1, kp2, features1, features2, 0.75, 4.0)

        if M == None:
            return None

        matches, H, status = M
        #sklejanie
        result = cv2.warpPerspective(image1, H,(image1.shape[1] + image2.shape[1], image1.shape[0]))
        result[0:image2.shape[0], 0:image2.shape[1]] = image2

        return result

#łączenie 8 zdjęć, najpierw parami , potem po 4
    def stitch8(self, images):
        results = []
        results2 = []
        for i in range(4):
            arg = [images[2 * i], images[2 * i + 1]]
            result = self.stitch(arg)
            results.append(result)
        for i in range(2):
            arg = [results[2 * i], results[2 * i + 1]]
            result = self.stitch(arg)
            results2.append(arg)
        result = self.stitch(results2)   # results2 jest puste, może gęściej zrobione zdjęcia pomogą

        return result
#dołączanie kolejnych zdjęć do pierwszego
    def stitch1(self, images):
        result = self.stitch((images[0],images[1]))
        for i in range(len(images) - 2):
            result = self.stitch((result, images[i + 2])) # po pierwszym result = none, jak wyżej, spróbować z gęstściej robionymi zdjęciami
        return result
#ta funkcja teoretycznie powinna być lepsza, nie mam pewności czy to przez liczbę zdjęć czy jakiś błąd
#dopasowuje do siebie ostatni dołączony obraz do kolejnego, a następnie go dołącza do już połączonych zdjęć
    def stitch2(self, images):
        ks = []
        features = []
        H = 1
        result = self.stitch((images[0], images[1]))
        for image in images:
            #image = images[i]
            k, f = self.detect(image)
            ks.append(k)
            features.append(f)
        for i in range(len(images) - 2):
            k1, features1 = self.detect(image[i + 1])
            k2, features2 = self.detect(image[i + 2])
            matches, h, status = self.match(k1, k2, features1, features2, 0.75, 4.0)
            H = H * h
            result = cv2.warpPerspective(result, H, (result.shape[1] + images[i].shape[1], result.shape[0]))
            result[0:images[i].shape[0], 0:images[i].shape[1]] = images[i]
        return result

    def detect(self, image):
        #wykrywanie punktów charakterystycznych
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()
        (k, features) = descriptor.detectAndCompute(image, None)

        k = np.float32([kp.pt for kp in k])

        return k, features

#dopasowanie obrazów
    def match(self, kpA, kpB, featureA, featureB, ratio, reproj):
        matcher = cv2.BFMatcher()
        rawmatches = matcher.knnMatch(featureA, featureB, k = 2)
        matches = []

        for  m in rawmatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 2:
            ptsA = np.float32([kpA[i] for (_,i) in matches])
            ptsB = np.float32([kpB[i] for (i,_) in matches])

            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reproj)

            return matches, H, status

        return None

#do testów

stitcher = Stitcher()
a = cv2.imread("0.jpg")
b = cv2.imread("1.jpg")
c = cv2.imread("2.jpg")
d = cv2.imread("3.jpg")
e = cv2.imread("4.jpg")
f = cv2.imread("5.jpg")
g = cv2.imread("6.jpg")
h = cv2.imread("7.jpg")
i = cv2.imread("8.jpg")

images = [a, b, c, d, e, f, g, h]
#result = stitcher.stitch8(images)
#result = stitcher.stitch((a,b))
#cv2.imshow("result", result)
#result = [stitcher.stitch((a, b)), stitcher.stitch((c, d)), stitcher.stitch((e, f)), stitcher.stitch((g, h))]
#result2 = [stitcher.stitch((result[0], result[1])), stitcher.stitch((result[2], result[3]))]
#result3 = stitcher.stitch(result2)
result4 = stitcher.stitch2(images)
cv2.imwrite("cos.jpg", result4)
cv2.waitKey(0)

