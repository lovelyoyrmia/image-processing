import io
import time
import numpy as np
import cv2
import streamlit as st
from PIL import Image
from random import randint

timeStr = time.strftime("%Y%m%d-%H%M%S")
idImage = str(randint(0, 1000))


def imageSt(image):
    return st.image(image, use_column_width=True)


def downloader(image):
    image_array = Image.fromarray(image)
    b = io.BytesIO()
    image_array.save(b, "JPEG")
    img_bytes = b.getvalue()
    return img_bytes


def imageDownloader(image):
    return st.download_button(
        "Download Image",
        image,
        "new_image_{}_{}.png".format(timeStr, idImage),
        mime="image/png",
    )


def imageConvertArray(image):
    image_array = np.array(image.convert("RGB"))
    image_download = cv2.cvtColor(image_array, 1)
    return image_download
