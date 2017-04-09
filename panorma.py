import numpy as np
import imutils
import cv2wrap

class Sticher:
    def __init__(self):
        self.isv3 = imutils.is_cv3()

    def stich(self, images):
        image11, image10, image9, image8, image7, image6, image5, image4, image3, image2, image1, image0 = images

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        descriptor = cv2.xfeatures2d.Shift_create()
        k, features = descriptor.detectAndCompute(image, none)

        k = np.float32([kp.pt for kp in k])

        return k, features


