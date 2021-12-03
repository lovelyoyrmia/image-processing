import cv2
import numpy as np
import streamlit as st
from emaskRcnn import loadImage


def colorQuantization(image, k):
    new_img = loadImage(image)
    # img_cvt = cv2.cvtColor(new_img, 1)
    data = np.float32(new_img).reshape((-1, 3))
    creteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(
        data, k, None, creteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(new_img.shape)

    return result


def edgeMask(image, line_size, blur_value):
    new_img = loadImage(image)
    img_cvt = cv2.cvtColor(new_img, 1)
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


def cartoonize(img):
    blur_value = st.sidebar.slider("Blur Value", 7, 10, key="blur_value")
    line_size = 7
    total_color = st.sidebar.slider("Total Color", 7, 15, key="line_size")

    edges = edgeMask(img, line_size, blur_value)
    img_quantization = colorQuantization(img, total_color)
    blurred = cv2.bilateralFilter(img_quantization, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return edges, img_quantization, blurred, cartoon
