import streamlit as st
import numpy as np
from about import aboutPage
import detections as dt
import time
from modules import Features, Download
from PIL import Image
from bgRemoval import removeBG
from emaskRcnn import maskImage
from sendEmail import sendEmail
from components import imageSt, imageSidebar


@st.cache()
def loadImagePIL(image_file):
    img = Image.open(image_file)
    return img


def main():
    image_logo = Image.open("assets/images.jpg")
    st.set_page_config(page_title="Image Procs",
                       page_icon=image_logo, layout="wide")
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

    activities = ["Processing", "Subscribe", "About"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    # === Subscribe Page ===
    if choice == "Subscribe":
        st.subheader("Let's get in touch")
        st.image("assets/images.jpg", width=400)
        email = st.text_input("Enter your email")
        if st.button("Subscribe"):
            with st.spinner("Sending email..."):
                sendEmail(email)

    # === Processing Page ===
    elif choice == "Processing":

        # st.subheader('Face Detection')
        image_file = st.file_uploader(
            "Upload Image", type=["png", "jpg", "jpeg"])

        if image_file is not None:

            img = loadImagePIL(image_file)

            features = Features(st, img)

            download = Download(st)

            img_grey = None
            img_contrast = None
            img_blur = None
            img_bright = None

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

                task = [
                    "Original Image",
                    "Face Detection",
                    "Smile Detection",
                    "Body and Object Detection",
                    "Mask R-CNN Image",
                ]
                option_task = st.sidebar.selectbox(
                    "Find Computer Vision Features", task
                )
                if option_task == "Original Image":
                    st.subheader("Original Image")
                    imageSt(img)

                elif option_task == "Face Detection":
                    if st.sidebar.button("Detect Faces"):
                        with st.spinner("Loading..."):
                            time.sleep(2)
                            result_img, faces = dt.detect_faces(img)
                            st.subheader("Results")
                            imageSt(result_img)
                            imageSidebar(img)
                            if len(faces) > 1:
                                st.success(f"Found {len(faces)} Faces")
                            else:
                                st.success(f"Found {len(faces)} Face")
                    else:
                        st.subheader("Original Image")
                        imageSt(img)

                elif option_task == "Smile Detection":
                    if st.sidebar.button("Detect Smiles"):
                        with st.spinner("Loading..."):
                            time.sleep(2)
                            result_smile = dt.detect_smiles(img)
                            st.subheader("Results")
                            imageSt(result_smile)
                            imageSidebar(img)
                    else:
                        st.subheader("Original Image")
                        imageSt(img)

                elif option_task == "Body and Object Detection":
                    if st.sidebar.button("Detect Bodies & Objects"):
                        with st.spinner("Loading..."):
                            time.sleep(2)
                            result_obj, _ = maskImage(img)
                            st.subheader("Results")
                            imageSt(result_obj)
                            imageSidebar(img)
                    else:
                        st.subheader("Original Image")
                        imageSt(img)

                else:
                    if st.sidebar.button("Mask Image"):
                        with st.spinner("Loading..."):
                            time.sleep(2)
                            _, result_mask = maskImage(img)
                            st.subheader("Masks")
                            imageSt(result_mask)
                            imageSidebar(img)
                    else:
                        st.subheader("Original Image")
                        imageSt(img)

            elif "Gray-Scale" in st.session_state.enchance:
                img_cvt_grey = features.greyscaleFeatures()
                st.subheader("Gray-Scale")
                imageSt(img_cvt_grey)
                img_bytes = download.downloader(img_cvt_grey)
                download.imageDownloader(img_bytes)

            elif "Contrast" in st.session_state.enchance:
                image_contrast = features.contrastFeatures()
                image_convert_arr = download.imageConvertArray(image_contrast)
                st.subheader("Contrast")
                imageSt(image_convert_arr)
                img_bytes = download.downloader(image_convert_arr)
                download.imageDownloader(img_bytes)

            elif "Brightness" in st.session_state.enchance:
                image_brightness = features.brightnessFeatures()
                image_convert_arr = download.imageConvertArray(image_brightness)
                st.subheader("Brightness")
                imageSt(image_convert_arr)
                img_bytes = download.downloader(image_convert_arr)
                download.imageDownloader(img_bytes)

            elif "Blurring" in st.session_state.enchance:
                img_blurring = features.blurrFeatures()
                st.subheader("Blurring")
                imageSt(img_blurring)
                img_bytes = download.downloader(img_blurring)
                download.imageDownloader(img_bytes)

            elif "Cartoonize" in st.session_state.enchance:
                features.cartoonFeatures()

            else:
                new_img = np.array(img)
                if st.sidebar.button("Remove Background"):
                    img_rmbg = removeBG(new_img)
                    st.subheader("Results")
                    imageSt(img_rmbg)
                    imageSidebar(img)
                    img_bytes = download.downloader(img_rmbg)
                    download.imageDownloader(img_bytes)
                else:
                    st.subheader("Original")
                    imageSt(img)

    # === About Page ===
    else:
        aboutPage(st)


if __name__ == "__main__":
    main()
