import io
import time
import numpy as np
import cv2
from PIL import Image
from random import randint


class Download:
    def __init__(self, st):
        self.st = st
        self.timeStr = time.strftime("%Y%m%d-%H%M%S")
        self.idImage = str(randint(0, 1000))

    def downloader(self, image, add_watermark=1):
        if add_watermark == 1:
            watermark = self.addWatermark(image)
            image_array = Image.fromarray(watermark)
        else:
            image_array = Image.fromarray(image)

        b = io.BytesIO()
        image_array.save(b, "JPEG")
        img_bytes = b.getvalue()

        return img_bytes

    def imageDownloader(self, image, sidebar=1):
        formatImg = self.formatDownload(sidebar).lower()

        if sidebar == 1:
            return self.st.sidebar.download_button(
                "Download Image",
                image,
                "new_image_{}_{}.{}".format(self.timeStr, self.idImage, formatImg),
                mime="image/{}".format(formatImg),
            )
        else:
            return self.st.download_button(
                "Download Image",
                image,
                "new_image_{}_{}.{}".format(self.timeStr, self.idImage, formatImg),
                mime="image/{}".format(formatImg),
            )

    def imageConvertArray(self, image):
        image_array = np.array(image.convert("RGB"))
        image_download = cv2.cvtColor(image_array, 1)

        return image_download

    def formatDownload(self, sidebar):
        if sidebar == 1:
            formatImg = self.st.sidebar.radio(
                "Choose Format Download Image", ["JPG", "PNG"]
            )
        else:
            formatImg = self.st.radio("Choose Format Download Image", ["JPG", "PNG"])

        return formatImg

    def scaleImg(self, image, scale_width):
        (img_height, img_width) = image.shape[:2]
        new_height = int(scale_width / img_width * img_height)

        return cv2.resize(image, (scale_width, new_height))

    def resizeImage(self, image, logo, h_img, w_img, h_logo, w_logo):
        percent_img_scale = 200
        new_h = int(h_img * percent_img_scale / 100)
        new_w = int(w_img * percent_img_scale / 100)
        resized_img = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

        logo_scale = 200
        logo_h = int(h_logo * logo_scale / 100)
        logo_w = int(w_logo * logo_scale / 100)
        resized_logo = cv2.resize(logo, (logo_w, logo_h), interpolation=cv2.INTER_AREA)

        return resized_img, resized_logo

    def addWatermark(self, image):
        logo = self.imageConvertArray(Image.open("assets/watermark.png"))

        if len(image.shape) == 3:
            logo = self.scaleImg(logo, 400)
        else:
            gray_logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
            logo = self.scaleImg(gray_logo, 400)

        (h_img, w_img) = image.shape[:2]
        (h_logo, w_logo) = logo.shape[:2]

        resized_img, resized_logo = self.resizeImage(
            image, logo, h_img, w_img, h_logo, w_logo
        )

        # Get Center Image
        (image_h, image_w) = resized_img.shape[:2]
        (wm_h, wm_w) = resized_logo.shape[:2]
        center_y = int(image_h / 2)
        center_x = int(image_w / 2)

        # Get top, left, right, bottom
        top_y = center_y - int(wm_h / 2)
        left_x = center_x - int(wm_w / 2)
        bottom_y = top_y + wm_h
        right_x = left_x + wm_w

        roi = resized_img[top_y:bottom_y, left_x:right_x]
        result = cv2.addWeighted(roi, 1, resized_logo, 0.3, 0)
        resized_img[top_y:bottom_y, left_x:right_x] = result

        return resized_img
