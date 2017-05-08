import numpy as np
import cv2

def stitch(ilosc_zdjec,number_resoult):

    images=[]
    for i in range(0,ilosc_zdjec+1):
        image = cv2.imread("../img/"+str(i)+".jpg")
        if image:
            images.append(image)
        else:
            print('brak zdjec - sklejanie jest niemozliwe')
            return



    for i in range(0,ilosc_zdjec+1):
        try:
            images[i] = images[i][:, int(0.1296296296 * images[i].shape[1]):int(0.8703703704 * images[i].shape[1])]
        except Exception as err:
            print(err)

    result = np.concatenate((images[0], images[1]), axis=1)

    for i in range(1,ilosc_zdjec):
            result = np.concatenate((result, images[i+1]), axis=1)

    x = result.shape[1]
    y = (x - result.shape[0])/2

    blackIm = create_blank(x,y)

    result = np.concatenate((result, blackIm), axis=0)
    result = np.concatenate((blackIm, result), axis=0)

    cv2.imwrite("streetView/vr/static_assets/result"+str(number_resoult)+".jpg", result)
    cv2.imwrite("result_last.jpg", result)
    # cv2.showImage(result)

def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image
