import streamlit as st
import numpy as np
import time
from modules import *
from PIL import Image


@st.cache()
def loadImagePIL(image_file):
    img = Image.open(image_file)
    return img


def processing():
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if image_file is not None:

        component = Components(st)
        download = Download(st)

        img = loadImagePIL(image_file)

        features = Features(st, img)

        st.session_state.enchance_type = [
            "Original",
            "Gray-Scale",
            "Contrast",
            "Brightness",
            "Blurring",
            "Cartoonize",
            "Remove-Background",
        ]

        st.session_state.enchance = st.sidebar.radio(
            "Enchance Type", st.session_state.enchance_type
        )

        if "Original" in st.session_state.enchance:
            detect = Detection(st)
            mask = MaskRcnn(st)

            task = [
                "Original Image",
                "Face Detection",
                "Smile Detection",
                "Body and Object Detection",
                "Mask R-CNN Image",
            ]

            option_task = st.sidebar.selectbox("Find Computer Vision Features", task)

            if option_task == "Original Image":
                component.imageSt(img, "Original Image")

            elif option_task == "Face Detection":
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

            elif option_task == "Smile Detection":
                if st.sidebar.button("Detect Smiles"):
                    with st.spinner("Loading..."):
                        time.sleep(2)
                        result_smile = detect.detectSmiles(img)
                        component.imageSt(result_smile, "Result")
                        component.imageSidebar(img)
                else:
                    component.imageSt(img, "Original Image")

            elif option_task == "Body and Object Detection":
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

        elif "Gray-Scale" in st.session_state.enchance:
            img_cvt_grey = features.greyscaleFeatures()
            component.imageSt(img_cvt_grey, "Gray Scale")
            img_bytes = download.downloader(img_cvt_grey)
            download.imageDownloader(img_bytes)

        elif "Contrast" in st.session_state.enchance:
            image_contrast = features.contrastFeatures()
            image_convert_arr = download.imageConvertArray(image_contrast)
            component.imageSt(image_convert_arr, "Contrast")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes)

        elif "Brightness" in st.session_state.enchance:
            image_brightness = features.brightnessFeatures()
            image_convert_arr = download.imageConvertArray(image_brightness)
            component.imageSt(image_convert_arr, "Brightness")
            img_bytes = download.downloader(image_convert_arr)
            download.imageDownloader(img_bytes)

        elif "Blurring" in st.session_state.enchance:
            img_blurring = features.blurrFeatures()
            component.imageSt(img_blurring, "Blurring")
            img_bytes = download.downloader(img_blurring)
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
                download.imageDownloader(img_bytes)
            else:
                component.imageSt(img, "Original Image")


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

    activities = ["Welcome", "Processing", "Get In Touch", "About"]
    navigation = st.sidebar.selectbox("Select Activity", activities)
    nav = Navigation(st)

    # === Welcome Page ===
    if navigation == "Welcome":
        nav.welcome()

    # === Processing Page ===
    elif navigation == "Processing":
        processing()

    # === Get In Touch Page ===
    elif navigation == "Get In Touch":
        nav.contact()

    # === About Page ===
    else:
        nav.aboutPage()


if __name__ == "__main__":
    main()
