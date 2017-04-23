import numpy as np
import cv2

def stitch(ilosc_zdjec,number_resoult):
    images=[]
    for i in range(0,ilosc_zdjec+1):
        images.append(cv2.imread("img/"+str(i)+".jpg"))

    for i in range(0,ilosc_zdjec+1):
        images[i] = images[i][:, int(0.1296296296 * images[i].shape[1]):int(0.8703703704 * images[i].shape[1])]

    result = images[0]

    for i in range(0,ilosc_zdjec):
        if i == 0:
            result = np.concatenate((images[i], images[i+1]), axis=1)
        else:
            result = np.concatenate((result, images[i+1]), axis=1)

    cv2.imwrite("result"+str(number_resoult)+".jpg", result)
    cv2.imwrite("result_last.jpg", result)
    # cv2.showImage(result)


