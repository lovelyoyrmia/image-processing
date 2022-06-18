import streamlit as st
import numpy as np
import time
import requests
from modules import *
from PIL import Image


@st.cache()
def loadImagePIL(image_file):
    try:
        img = Image.open(image_file)
    except Exception:
        img = None

    return img


def loadImageUrl(image_file):
    img = None

    try:
        response = requests.get(image_file, stream=True)
        try:
            download = Download(st)
            img = Image.open(response.raw)
            arr_img = download.imageConvertArray(img)
            scale = download.scaleImg(arr_img, 800)
            img = Image.fromarray(scale)

        except Exception:
            st.error("Cannot load your image. Please try again !")
            img = None

    except Exception:
        st.error("Please Input The Valid URL")
        img = None

    return img


def uploader():
    image_file = None
    img = None
    choose_upload = st.selectbox(
        "Choose option to upload", ["Choose Type", "Drag and Drop", "Upload From Url"]
    )

    if choose_upload == "Choose Type":
        image_file = None
        img = None

    elif choose_upload == "Drag and Drop":
        image_drag = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        img = loadImagePIL(image_drag)
        image_file = image_drag

    else:
        image_url = st.text_input("Input Url Image")

        if image_url != "":
            img = loadImageUrl(image_url)

            if img is None:
                image_file = None
            else:
                image_file = image_url

            return img, image_file

        else:
            image_url = None

        image_file = image_url

    return img, image_file


def processing():
    img, image_file = uploader()
    img_bytes = None

    # ALL VARIABLES CLASS
    component = Components(st)
    download = Download(st)
    features = Features(st, img)

    if image_file is not None:
        st.session_state.enchance_type = [
            "Original",
            "Gray-Scale",
            "Contrast",
            "Brightness",
            "Blurring",
            "Thresholding",
            "Hue And Saturation",
            "Canny Edge",
            "Cartoonize",
            "Remove-Background",
        ]

        st.session_state.enchance = st.sidebar.radio(
            "Enchance Type", st.session_state.enchance_type
        )

        if "Original" in st.session_state.enchance:
            image_original = download.imageConvertArray(img)
            component.imageSt(image_original, "Original Image")
            img_bytes = download.downloader(image_original, 0)
            download.imageDownloader(img_bytes)

        elif "Gray-Scale" in st.session_state.enchance:
            img_gray = features.greyscaleFeatures()
            component.imageColumn(img,img_gray, "Gray Scale")
            img_bytes = download.downloader(img_gray)
            download.imageDownloader(img_bytes, 1)

        elif "Contrast" in st.session_state.enchance:
            image_contrast = features.contrastFeatures()
            image_convert_arr = download.imageConvertArray(image_contrast)
            component.imageColumn(img, image_convert_arr, "Contrast")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes, 1)

        elif "Brightness" in st.session_state.enchance:
            img_bright = features.brightnessFeatures()
            image_convert_arr = download.imageConvertArray(img_bright)
            component.imageColumn(img, image_convert_arr, "Brightness")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes, 1)

        elif "Blurring" in st.session_state.enchance:
            img_blurring = features.blurrFeatures()
            component.imageColumn(img, img_blurring, "Blurring")
            img_bytes = download.downloader(img_blurring)
            download.imageDownloader(img_bytes, 1)

        elif "Thresholding" in st.session_state.enchance:
            img_thresh = features.thresholding()
            component.imageColumn(img, img_thresh, "Thresholding")
            img_bytes = download.downloader(img_thresh)
            download.imageDownloader(img_bytes)

        elif "Hue And Saturation" in st.session_state.enchance:
            img_hue_sat = features.hueAndSaturation()
            component.imageColumn(img, img_hue_sat, "Hue And Saturation Color")
            img_bytes = download.downloader(img_hue_sat)
            download.imageDownloader(img_bytes)

        elif "Canny Edge" in st.session_state.enchance:
            edges = features.cannyEdge()
            component.imageColumn(img, edges, "Canny Edge")
            img_bytes = download.downloader(edges)
            download.imageDownloader(img_bytes)

        elif "Cartoonize" in st.session_state.enchance:
            features.cartoonFeatures()

        else:
            remove = RemoveBg()
            new_img = np.array(img)
            if st.sidebar.button("Remove Background"):
                img_rmbg = remove.removeBG(new_img)
                component.imageColumn(img, img_rmbg, "Remove Background")
                img_bytes = download.downloader(img_rmbg)
                download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")
    else:
        st.info("Please Upload Your Image")


def computerVisionFeatures():
    img, image_file = uploader()
    # ALL VARIABLES CLASS
    component = Components(st)
    download = Download(st)

    if image_file is not None:
        # ALL VARIABLES FOR COMPUTER VISION
        detect = Detection(st)
        mask = MaskRcnn(st)

        st.session_state.task = [
            "Original Image",
            "Face Detection",
            "Smile Detection",
            "Eyes Detection",
            "Body and Object Detection",
            "Mask R-CNN Image",
        ]

        st.session_state.option_task = st.sidebar.radio(
            "Find Computer Vision Features", st.session_state.task
        )

        if "Original Image" in st.session_state.option_task:
            component.imageSt(img, "Original Image")

        elif "Face Detection" in st.session_state.option_task:
            if st.sidebar.button("Detect Faces"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    result_img, faces = detect.detectFaces(img)
                    component.imageColumn(img, result_img, "Result")
                    img_bytes = download.downloader(result_img)
                    download.imageDownloader(img_bytes)
                    if len(faces) > 1:
                        st.success(f"Found {len(faces)} Faces")
                    else:
                        st.success(f"Found {len(faces)} Face")
            else:
                component.imageSt(img, "Original Image")

        elif "Smile Detection" in st.session_state.option_task:
            if st.sidebar.button("Detect Smiles"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    result_smile = detect.detectSmiles(img)
                    component.imageColumn(img, result_smile, "Result")
                    img_bytes = download.downloader(result_smile)
                    download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")

        elif "Eyes Detection" in st.session_state.option_task:
            if st.sidebar.button("Detect Eyes"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    result_eyes = detect.detectEye(img)
                    component.imageColumn(img, result_eyes, "Result")
                    img_bytes = download.downloader(result_eyes)
                    download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")

        elif "Body and Object Detection" in st.session_state.option_task:
            if st.sidebar.button("Detect Bodies & Objects"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    result_obj, _ = mask.maskImage(img)
                    component.imageColumn(img, result_obj, "Result")
                    img_bytes = download.downloader(result_obj)
                    download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")

        else:
            if st.sidebar.button("Mask Image"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    _, result_mask = mask.maskImage(img)
                    component.imageColumn(img, result_mask, "Mask Image")
                    img_bytes = download.downloader(result_mask)
                    download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")
    else:
        st.info("Please Upload Your Image")
