import numpy as np
import imutils
import cv2
import argparse


#############################
#trzeba przetestować
#############################

class Stitcher:
    def __init__(self):
        self.isv3 = imutils.is_cv3()

    def stitch(self, images):
        image2, image1 = images #w liście zdjęcia od lewej do prawej
        kp1, features1 = self.detect(image1)
        kp2, features2 = self.detect(image2)

        M = self.match(kp1, kp2, features1, features2, 0.75, 4.0)

        if M == None:
            return None

        (matches, H, status) = M
        result = cv2.warpPerspective(image1, H,(image1.shape[1] + image2.shape[1], image1.shape[0]))
        result[0:image2.shape[0], 0:image2.shape[1]] = image2

        return result

    def detect(self, image):
        #wykrywanie punktów charakterystycznych
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()
        (k, features) = descriptor.detectAndCompute(image, None)

        k = np.float32([kp.pt for kp in k])

        return k, features

    def match(self, kpA, kpB, featureA, featureB, ratio, reproj):
        matcher = cv2.BFMatcher()
        rawmatches = matcher.knnMatch(featureA, featureB, k = 2)
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



imageA = cv2.imread("test2.jpg")
imageB = cv2.imread("test1.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

stitcher = Stitcher()
result1 = stitcher.stitch([imageA, imageB])
#cv2.imshow("Result", result1)

imageA = cv2.imread("test3.jpg")
imageB = cv2.imread("test4.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

result2 = stitcher.stitch([imageA, imageB])


imageA = cv2.imread("test5.jpg")
imageB = cv2.imread("test6.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

result3 = stitcher.stitch([imageA, imageB])


imageA = cv2.imread("test7.jpg")
imageB = cv2.imread("test8.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

result4 = stitcher.stitch([imageA, imageB])


imageA = cv2.imread("test9.jpg")
imageB = cv2.imread("test10.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

result5 = stitcher.stitch([imageA, imageB])


imageA = cv2.imread("test12.jpg")
imageB = cv2.imread("test11.jpg")
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

result6 = stitcher.stitch([imageA, imageB])


result7 = stitcher.stitch([result1, result6])
result8 = stitcher.stitch([result3, result2])
#result9 = stitcher.stitch([result5, result4])
cv2.imshow("Result", result8)
cv2.imwrite("result.jpg", result7)
cv2.waitKey(0)

