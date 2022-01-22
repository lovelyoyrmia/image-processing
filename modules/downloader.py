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

    def downloader(self, image):
        image_array = Image.fromarray(image)
        b = io.BytesIO()
        image_array.save(b, "JPEG")
        img_bytes = b.getvalue()
        return img_bytes

    def imageDownloader(self, image, sidebar=0):
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
