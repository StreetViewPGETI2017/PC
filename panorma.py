import numpy as np
import imutils
import cv2wrap as cv2
#nie testowane

class Sticher:
    def __init__(self):
        self.isv3 = imutils.is_cv3()

    def stich(self, images):
        image11, image10, image9, image8, image7, image6, image5, image4, image3, image2, image1, image0 = images #w liście zdjęcia od lewej do prawej

    def detect(self, image):
        #wykrywanie punktów charakterystycznych
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        descriptor = cv2.xfeatures2d.Shift_create()
        k, features = descriptor.detectAndCompute(image)

        k = np.float32([kp.pt for kp in k])

        return k, features

    def match(self, kpA, kpB, featureA, featureB, ratio, reproj):
        matcher = cv2.DescriptionMatcher_cerate("Bruteforce")
        rawmatches = matcher.knnMatch(featureA, featureB, 2)
        matches = []

        for  m in rawmatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 4:
            ptsA = np.float32([kpA[i] for (_,i) in matches])
            ptsB = np.float32([kpB[i] for (i,_) in matches])

            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reproj)

            return matches, H, status

        return None
