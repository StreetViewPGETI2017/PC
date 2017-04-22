import numpy as np
import cv2

def stitch():
    a = cv2.imread("0.jpg")
    b = cv2.imread("1.jpg")
    c = cv2.imread("2.jpg")
    d = cv2.imread("3.jpg")
    e = cv2.imread("4.jpg")
    f = cv2.imread("5.jpg")
    g = cv2.imread("6.jpg")
    h = cv2.imread("7.jpg")
    i = cv2.imread("8.jpg")

    a = a[:,0.1296296296 * a.shape[1]:0.8703703704 * a.shape[1]]
    b = b[:,0.1296296296 * b.shape[1]:0.8703703704 * b.shape[1]]
    c = c[:,0.1296296296 * c.shape[1]:0.8703703704 * c.shape[1]]
    d = d[:,0.1296296296 * d.shape[1]:0.8703703704 * d.shape[1]]
    e = e[:,0.1296296296 * e.shape[1]:0.8703703704 * e.shape[1]]
    f = f[:,0.1296296296 * f.shape[1]:0.8703703704 * f.shape[1]]
    g = g[:,0.1296296296 * g.shape[1]:0.8703703704 * g.shape[1]]
    h = h[:,0.1296296296 * h.shape[1]:0.8703703704 * h.shape[1]]
    i = i[:,0.1296296296 * i.shape[1]:0.8703703704 * i.shape[1]]

    result = np.concatenate((a, b), axis=1)
    result = np.concatenate((result, c), axis=1)
    result = np.concatenate((result, d), axis=1)
    result = np.concatenate((result, e), axis=1)
    result = np.concatenate((result, f), axis=1)
    result = np.concatenate((result, g), axis=1)
    result = np.concatenate((result, h), axis=1)
    result = np.concatenate((result, i), axis=1)

    cv2.imwrite("cos.jpg", result)



