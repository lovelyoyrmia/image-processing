import cv2
import numpy as np
from PIL import ImageEnhance
from cartoons import cartoonize
from downloader import Download
from components import imageSidebar, imageSt


class Features:
    def __init__(self, st, img):
        self.st = st
        self.img = img

    def greyscaleFeatures(self):
        new_img = np.array(self.img.convert("RGB"))
        img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

        return img_cvt

    def contrastFeatures(self):
        c_rate = self.st.sidebar.slider(
            "Contrast", 0.5, 3.5, step=0.5, key="contrast"
        )
        enchancer = ImageEnhance.Contrast(self.img)
        img_contrast = enchancer.enhance(c_rate)
        
        return img_contrast


    def brightnessFeatures(self):
        c_rate = self.st.sidebar.slider(
            "Brightness", 0.5, 3.5, step=0.5, key="brightness"
        )
        enchancer = ImageEnhance.Brightness(self.img)
        img_brightness = enchancer.enhance(c_rate)
        
        return img_brightness


    def blurrFeatures(self):
        blur_rate = self.st.sidebar.slider(
            "Blurring", 0.5, 3.5, step=0.5, key="blurring"
        )
        new_img = np.array(self.img.convert("RGB"))
        img_blur = cv2.GaussianBlur(new_img, (11, 11), blur_rate)
        
        return img_blur

    def cartoonFeatures(self):
        features_cartoon = [
            "Original",
            "Sketch",
            "Color Quantization",
            "Quantization Blurred",
            "Cartoons",
        ]
        type_cartoonize = self.st.sidebar.selectbox(
            "Types Of Cartoonize", features_cartoon
        )

        edges, img_quantization, blurred, cartoon = cartoonize(self.img)

        download = Download(self.st)

        if type_cartoonize == "Original":
            self.st.subheader("Original")
            imageSt(self.img)

        elif type_cartoonize == "Sketch":
            if self.st.sidebar.button('Process'):
                self.st.subheader("Result Sketch")
                imageSt(edges)
                img_bytes = download.downloader(edges)
                imageSidebar(self.img)
                download.imageDownloader(img_bytes)
            else:
                self.st.subheader("Original")
                imageSt(self.img)
        elif type_cartoonize == "Color Quantization":
            if self.st.sidebar.button('Process'):
                self.st.subheader("Result Image Quantization")
                imageSt(img_quantization)
                img_bytes = download.downloader(img_quantization)
                imageSidebar(self.img)
                download.imageDownloader(img_bytes)
            else:
                self.st.subheader("Original")
                imageSt(self.img)
        elif type_cartoonize == "Quantization Blurred":
            if self.st.sidebar.button('Process'):
                self.st.subheader("Result Image Quantization Blurred")
                imageSt(blurred)
                img_bytes = download.downloader(blurred)
                imageSidebar(self.img)
                download.imageDownloader(img_bytes)
            else:
                self.st.subheader("Original")
                imageSt(self.img)
        elif type_cartoonize == "Cartoons":
            if self.st.sidebar.button('Process'):
                self.st.subheader("Result Image Cartoon")
                imageSt(cartoon)
                img_bytes = download.downloader(cartoon)
                imageSidebar(self.img)
                download.imageDownloader(img_bytes)
        else:
            self.st.subheader("Original")
            imageSt(self.img)
