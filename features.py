import streamlit as st
import cv2
import numpy as np
from PIL import ImageEnhance
from downloader import *
from cartoons import cartoonize


def greyscaleFeatures(img):
    new_img = np.array(img.convert("RGB"))
    img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    st.subheader("Gray-Scale")
    imageSt(img_cvt)
    img_bytes = downloader(img_cvt)
    imageDownloader(img_bytes)


def contrastFeatures(img):
    c_rate = st.sidebar.slider(
        "Contrast", 0.5, 3.5, step=0.5, key="contrast"
    )
    enchancer = ImageEnhance.Contrast(img)
    img_contrast = enchancer.enhance(c_rate)
    image_download = imageConvertArray(img_contrast)
    st.subheader("Contrast")
    imageSt(image_download)
    img_bytes = downloader(image_download)
    imageDownloader(img_bytes)


def brightnessFeatures(img):
    c_rate = st.sidebar.slider(
        "Brightness", 0.5, 3.5, step=0.5, key="brightness"
    )
    enchancer = ImageEnhance.Brightness(img)
    img_brightness = enchancer.enhance(c_rate)
    image_download = imageConvertArray(img_brightness)
    st.subheader("Brightness")
    imageSt(image_download)
    img_bytes = downloader(image_download)
    imageDownloader(img_bytes)


def blurrFeatures(img):
    blur_rate = st.sidebar.slider(
        "Blurring", 0.5, 3.5, step=0.5, key="blurring"
    )
    new_img = np.array(img.convert("RGB"))
    img_blur = cv2.GaussianBlur(new_img, (11, 11), blur_rate)
    st.subheader("Blurring")
    imageSt(img_blur)
    img_bytes = downloader(img_blur)
    imageDownloader(img_bytes)


def cartoonFeatures(img):
    features_cartoon = [
        "Original",
        "Sketch",
        "Color Quantization",
        "Quantization Blurred",
        "Cartoons",
    ]
    type_cartoonize = st.sidebar.selectbox(
        "Types Of Cartoonize", features_cartoon
    )

    edges, img_quantization, blurred, cartoon = cartoonize(img)

    if type_cartoonize == "Original":
        st.subheader("Original")
        imageSt(img)

    elif type_cartoonize == "Sketch":
        if st.sidebar.button('Process'):
            st.subheader("Result Sketch")
            imageSt(edges)
            img_bytes = downloader(edges)
            imageSidebar(img)
            imageDownloader(img_bytes)
        else:
            st.subheader("Original")
            imageSt(img)
    elif type_cartoonize == "Color Quantization":
        if st.sidebar.button('Process'):
            st.subheader("Result Image Quantization")
            imageSt(img_quantization)
            img_bytes = downloader(img_quantization)
            imageSidebar(img)
            imageDownloader(img_bytes)
        else:
            st.subheader("Original")
            imageSt(img)
    elif type_cartoonize == "Quantization Blurred":
        if st.sidebar.button('Process'):
            st.subheader("Result Image Quantization Blurred")
            imageSt(blurred)
            img_bytes = downloader(blurred)
            imageSidebar(img)
            imageDownloader(img_bytes)
        else:
            st.subheader("Original")
            imageSt(img)
    elif type_cartoonize == "Cartoons":
        if st.sidebar.button('Process'):
            st.subheader("Result Image Cartoon")
            imageSt(cartoon)
            img_bytes = downloader(cartoon)
            imageSidebar(img)
            imageDownloader(img_bytes)
        else:
            st.subheader("Original")
            imageSt(img)
