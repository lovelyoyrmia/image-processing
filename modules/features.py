import cv2
import numpy as np
import time
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

    def cannyEdge(self):
        img = self.component.cvtImgToArr(self.img)
        thresh1 = self.st.sidebar.slider("Threshold 1", 0, 200)
        thresh2 = self.st.sidebar.slider("Threshold 2", 0, 200)
        edges = cv2.Canny(img, thresh1, thresh2)

        return edges

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

        download = Download(self.st)

        line_size = 5

        total_color = 2

        blur_value = 1

        if type_cartoonize == "Sketch" or type_cartoonize == "Cartoons":
            line_size = self.st.sidebar.slider("Line Size Value", line_size, 17, step=2)

        if type_cartoonize == "Color Quantization" or type_cartoonize == "Cartoons":
            total_color = self.st.sidebar.slider("Total Color Value", total_color, 20)

        if type_cartoonize == "Quantization Blurred" or type_cartoonize == "Cartoons":
            blur_value = self.st.sidebar.slider("Blurred Value", blur_value, 15, step=2)

        edges, img_quantization, blurred, cartoon = cartoons.cartoonize(
            self.img, line_size, total_color, blur_value
        )

        if type_cartoonize == "Original":
            self.component.imageSt(self.img, "Original Image")

        elif type_cartoonize == "Sketch":
            with self.st.spinner("Wait a sec...."):
                time.sleep(4)
                self.component.imageColumn(self.img, edges, "Result Sketch")
            img_bytes = download.downloader(edges)
            download.imageDownloader(img_bytes)

        elif type_cartoonize == "Color Quantization":
            with self.st.spinner("Wait a sec...."):
                time.sleep(4)
                self.component.imageColumn(self.img, img_quantization, "Result Image Quantization")
            img_bytes = download.downloader(img_quantization)
            download.imageDownloader(img_bytes)

        elif type_cartoonize == "Quantization Blurred":
            with self.st.spinner("Wait a sec...."):
                time.sleep(4)
                self.component.imageColumn(self.img, blurred, "Result Image Quantization Blurred")
            img_bytes = download.downloader(blurred)
            download.imageDownloader(img_bytes)

        else:
            with self.st.spinner("Wait a sec...."):
                time.sleep(4)
                self.component.imageColumn(self.img, cartoon, "Result Image Cartoon")
            img_bytes = download.downloader(cartoon)
            download.imageDownloader(img_bytes)
