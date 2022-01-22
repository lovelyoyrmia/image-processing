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
