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

@st.cache()
def loadImageUrl(image_file):
    try:
        response = requests.get(image_file, stream=True)
        img = Image.open(response.raw)
    except Exception:
        st.error('Please Input The Valid URL')

    return img


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
            "Cartoonize",
            "Remove-Background",
        ]

        st.session_state.enchance = st.sidebar.radio(
            "Enchance Type", st.session_state.enchance_type
        )

        if "Original" in st.session_state.enchance:
            component.imageSt(img, "Original Image")

        elif "Gray-Scale" in st.session_state.enchance:
            img_gray = features.greyscaleFeatures()
            component.imageSt(img_gray, "Gray Scale")
            img_bytes = download.downloader(img_gray)
            download.imageDownloader(img_bytes, 1)

        elif "Contrast" in st.session_state.enchance:
            image_contrast = features.contrastFeatures()
            image_convert_arr = download.imageConvertArray(image_contrast)
            component.imageSt(image_convert_arr, "Contrast")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes, 1)

        elif "Brightness" in st.session_state.enchance:
            image_brightness = features.brightnessFeatures()
            image_convert_arr = download.imageConvertArray(image_brightness)
            component.imageSt(image_convert_arr, "Brightness")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes, 1)

        elif "Blurring" in st.session_state.enchance:
            img_blurring = features.blurrFeatures()
            component.imageSt(img_blurring, "Blurring")
            img_bytes = download.downloader(img_blurring)
            download.imageDownloader(img_bytes, 1)

        elif "Thresholding" in st.session_state.enchance:
            img_thresh = features.thresholding()
            component.imageSt(img_thresh, "Thresholding")
            component.imageSidebar(img)
            img_bytes = download.downloader(img_thresh)
            download.imageDownloader(img_bytes)

        elif "Hue And Saturation" in st.session_state.enchance:
            img_hue_sat = features.hueAndSaturation()
            component.imageSt(img_hue_sat, "Hue And Saturation Color")
            component.imageSidebar(img)
            img_bytes = download.downloader(img_hue_sat)
            download.imageDownloader(img_bytes)

        elif "Cartoonize" in st.session_state.enchance:
            features.cartoonFeatures()

        else:
            remove = RemoveBg()
            new_img = np.array(img)
            if st.sidebar.button("Remove Background"):
                img_rmbg = remove.removeBG(new_img)
                component.imageSt(img_rmbg, "Result")
                component.imageSidebar(img)
                img_bytes = download.downloader(img_rmbg)
                download.imageDownloader(img_bytes, 1)
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
                    component.imageSt(result_img, "Result")
                    component.imageSidebar(img)
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
                    component.imageSt(result_smile, "Result")
                    component.imageSidebar(img)
            else:
                component.imageSt(img, "Original Image")

        elif "Body and Object Detection" in st.session_state.option_task:
            if st.sidebar.button("Detect Bodies & Objects"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    result_obj, _ = mask.maskImage(img)
                    component.imageSt(result_obj, "Result")
                    component.imageSidebar(img)
            else:
                component.imageSt(img, "Original Image")

        else:
            if st.sidebar.button("Mask Image"):
                with st.spinner("Loading..."):
                    time.sleep(2)
                    _, result_mask = mask.maskImage(img)
                    component.imageSt(result_mask, "Mask Image")
                    img_bytes = download.downloader(result_mask)
                    download.imageDownloader(img_bytes)
                    component.imageSidebar(img)
            else:
                component.imageSt(img, "Original Image")
    else:
        st.info("Please Upload Your Image")


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
        else:
            image_url = None

        image_file = image_url

    return img, image_file


def main():
    image_logo = Image.open("assets/images.jpg")
    st.set_page_config(page_title="Image Procs", page_icon=image_logo, layout="wide")
    hide_menu_style = """
    <style>
        #MainMenu {display: none; }
        footer {visibility: hidden;}
        .css-fk4es0 {display: none;}
        #stStatusWidget {display: none;}
        .css-r698ls {display: none;}
    </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # ==== Image Processing ====
    st.title("Image Processing App")
    st.text("Build using Computer Vision and Artificial Intelligence")

    activities = [
        "Welcome",
        "Processing",
        "Computer Vision Features",
        "Get In Touch",
        "About",
    ]
    navigation = st.sidebar.selectbox("Select Activity", activities)
    nav = Navigation(st)

    # ALL VARIABLES IMAGE

    # === Welcome Page ===
    if navigation == "Welcome":
        nav.welcome()

    # === Processing Page ===
    elif navigation == "Processing":
        processing()

    elif navigation == "Computer Vision Features":
        computerVisionFeatures()

    # === Get In Touch Page ===
    elif navigation == "Get In Touch":
        nav.contact()

    # === About Page ===
    else:
        nav.aboutPage()


if __name__ == "__main__":
    main()
