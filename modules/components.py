import numpy as np


class Components:
    def __init__(self, st):
        self.st = st

    def cvtImgToArr(self, image):
        img = np.array(image.convert("RGB"))
        return img

    def imageSt(self, image, title):
        self.st.subheader(title)
        self.st.image(image, use_column_width=True, clamp=True)

    def imageSidebar(self, image):
        self.st.sidebar.subheader("Original")
        self.st.sidebar.image(image, use_column_width=True, clamp=True)

    def imageColumn(self, image1, image2, title2, title1='Original'):
        col1, col2 = self.st.columns([2, 2])
        col1.subheader(title1)
        col1.image(image1, use_column_width=True, clamp=True)

        col2.subheader(title2)
        col2.image(image2, use_column_width=True, clamp=True)