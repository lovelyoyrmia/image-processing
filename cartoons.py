import cv2
import numpy as np
from emaskRcnn import loadImage


def colorQuantization(image, k):
    # new_img = loadImage(image)
    data = np.float32(image).reshape((-1, 3))
    creteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(
        data, k, None, creteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(image.shape)

    return result


def edgeMask(image, line_size, blur_value):
    # new_img = loadImage(image)
    img_cvt = cv2.cvtColor(image, 1)
    gray = cv2.cvtColor(img_cvt, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(
        gray_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        line_size,
        blur_value,
    )
    return edges


img = cv2.imread("vio.jpg")

line_size = 7
blur_value = 7

edges = edgeMask(img, line_size, blur_value)

total_color = 11
img = colorQuantization(img, total_color)
cv2.imshow("", img)
cv2.waitKey(0)

blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)

cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
