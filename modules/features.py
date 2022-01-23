import cv2
import numpy as np
from PIL import ImageEnhance
from modules.cartoons import Cartoons
from modules.components import Components
from modules.downloader import Download


class Features:
    def __init__(self, st, img):
        self.st = st
        self.img = img
        self.component = Components(self.st)

    def greyscaleFeatures(self):
        new_img = self.component.cvtImgToArr(self.img)
        img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

        return img_cvt

    def contrastFeatures(self):
        c_rate = self.st.sidebar.slider("Contrast", 0.5, 3.5, step=0.5)
        enchancer = ImageEnhance.Contrast(self.img)
        img_contrast = enchancer.enhance(c_rate)

        return img_contrast

    def brightnessFeatures(self):
        c_rate = self.st.sidebar.slider("Brightness", 0.5, 3.5, step=0.5)
        enchancer = ImageEnhance.Brightness(self.img)
        img_brightness = enchancer.enhance(c_rate)

        return img_brightness

    def blurrFeatures(self):
        blur_rate = self.st.sidebar.slider("Blurring", 0.5, 3.5, step=0.5)
        new_img = np.array(self.img.convert("RGB"))
        img_blur = cv2.GaussianBlur(new_img, (11, 11), blur_rate)

        return img_blur

    def thresholding(self):
        new_img = self.component.cvtImgToArr(self.img)
        img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        value = self.st.sidebar.slider("Change Threshold Value", 0, 255)
        _, img_thresh = cv2.threshold(img_cvt, value, 255, cv2.THRESH_BINARY)

        return img_thresh

    def hueAndSaturation(self):
        img = np.asarray(self.img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hue_value = self.st.sidebar.slider("Change Hue Value", 0, 255)
        saturation_value = self.st.sidebar.slider("Change Saturation Value", 0, 255)

        table_hue = (
            np.array([i + 1 * hue_value for i in range(0, 256)])
            .clip(0, 255)
            .astype("uint8")
        )
        table_saturation = (
            np.array([i * saturation_value for i in range(0, 256)])
            .clip(0, 255)
            .astype("uint8")
        )
        img_hsv[:, :, 0] = cv2.LUT(img_hsv[:, :, 0], table_hue)
        img_hsv[:, :, 1] = cv2.LUT(img_hsv[:, :, 1], table_saturation)
        img_ret = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)

        return img_ret

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

        cartoons = Cartoons(self.st)

        edges, img_quantization, blurred, cartoon = cartoons.cartoonize(self.img)

        download = Download(self.st)

        if type_cartoonize == "Original":
            self.component.imageSt(self.img, "Original Image")

        elif type_cartoonize == "Sketch":
            if self.st.sidebar.button("Process"):
                with self.st.spinner("Wait a sec...."):
                    self.component.imageSt(edges, "Result Sketch")
                    self.component.imageSidebar(self.img)
                img_bytes = download.downloader(edges)
                download.imageDownloader(img_bytes)
            else:
                self.component.imageSt(self.img, "Original Image")

        elif type_cartoonize == "Color Quantization":
            if self.st.sidebar.button("Process"):
                with self.st.spinner("Wait a sec...."):
                    self.component.imageSt(
                        img_quantization, "Result Image Quantization"
                    )
                    self.component.imageSidebar(self.img)
                img_bytes = download.downloader(img_quantization)
                download.imageDownloader(img_bytes)
            else:
                self.component.imageSt(self.img, "Original Image")

        elif type_cartoonize == "Quantization Blurred":
            if self.st.sidebar.button("Process"):
                with self.st.spinner("Wait a sec...."):
                    self.component.imageSt(blurred, "Result Image Quantization Blurred")
                    self.component.imageSidebar(self.img)
                img_bytes = download.downloader(blurred)
                download.imageDownloader(img_bytes)
            else:
                self.component.imageSt(self.img, "Original Image")

        else:
            if self.st.sidebar.button("Process"):
                with self.st.spinner("Wait a sec...."):
                    self.component.imageSt(cartoon, "Result Image Cartoon")
                    self.component.imageSidebar(self.img)
                img_bytes = download.downloader(cartoon)
                download.imageDownloader(img_bytes)
            else:
                self.component.imageSt(self.img, "Original Image")
