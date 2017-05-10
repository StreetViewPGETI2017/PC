import numpy as np
import cv2

def stitch(ilosc_zdjec,number_resoult):

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

    for i in range(0,ilosc_zdjec+1):
        try:
            #images[i] = images[i][:, int(0.1296296296 * images[i].shape[1]):int(0.8703703704 * images[i].shape[1])]
            images[i] = images[i][:, int(lewy * images[i].shape[1]):int(prawy * images[i].shape[1])]
            cv2.imshow("ob", images[i])
            cv2.waitKey(0)
        except Exception as err:
            print(err)

    result = np.concatenate((images[0], images[1]), axis=1)

    for i in range(1,ilosc_zdjec):
        try:
            result = np.concatenate((result, images[i+1]), axis=1)

        except Exception as err:
            print(err)

    x = result.shape[1]
    y = (x - result.shape[0])/2

    blackIm = create_blank(x,y)

    result = np.concatenate((result, blackIm), axis=0)
    result = np.concatenate((blackIm, result), axis=0)

    cv2.imwrite("streetView/vr/static_assets/result"+str(number_resoult)+".jpg", result)
    cv2.imwrite("result_last.jpg", result)
    # cv2.showImage(result)

def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((int(height), int(width), 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def detect(image):
    # wykrywanie punktów charakterystycznych
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    descriptor = cv2.xfeatures2d.SIFT_create()
    (k, features) = descriptor.detectAndCompute(image, None)

    k = np.float32([kp.pt for kp in k])

    return k, features


def match(kpA, kpB, featureA, featureB, ratio, reproj):
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

def stitching(images):
    image2, image1 = images  # w liście zdjęcia od lewej do prawej
    kp1, features1 = detect(image1)
    kp2, features2 = detect(image2)

    M = match(kp1, kp2, features1, features2, 0.75, 4.0)
    if M == None:
        return None

    matches, H, status = M
    result = cv2.warpPerspective(image1, H, (image1.shape[1] + image2.shape[1], image1.shape[0]))
    result[0:image2.shape[0], 0:image2.shape[1]] = image2
    return result

def uberStitching(ilosc_zdjec,number_resoult):
    if ilosc_zdjec + 1 < 16:
        stitch(ilosc_zdjec, number_resoult)
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
        for i in range((ilosc_zdjec + 1)/2):
            obrazki = (images[2 * i], images[2 * i + 1])
            obrazek = stitching(obrazki)
            zlaczone.append(obrazek)

        liczba = len(zlaczone)
        ile = (360 / liczba) / 54
        lewy = (1 - ile) / 2
        prawy = 1 - lewy

        for i in range(0, liczba):
            try:
                images[i] = images[i][:, int(lewy * images[i].shape[1]):int(prawy * images[i].shape[1])]
            except Exception as err:
                print(err)

        result = np.concatenate((images[0], images[1]), axis=1)

        for i in range(1, liczba - 1):
            result = np.concatenate((result, images[i + 1]), axis=1)

        x = result.shape[1]
        y = (x - result.shape[0]) / 2

        blackIm = create_blank(x, y)

        result = np.concatenate((result, blackIm), axis=0)
        result = np.concatenate((blackIm, result), axis=0)

        cv2.imwrite("streetView/vr/static_assets/result" + str(number_resoult) + ".jpg", result)
        cv2.imwrite("result_last.jpg", result)


