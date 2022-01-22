import cv2
import mediapipe as mp
import numpy as np


class RemoveBg:
    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_segment = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_segment.SelfieSegmentation()

    def removeBG(self, img, img_Bg=(255, 255, 255), threshold=0.1):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.selfie_segmentation.process(img_RGB)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > threshold
        if isinstance(img_Bg, tuple):
            _imgBg = np.zeros(img.shape, dtype=np.uint8)
            _imgBg[:] = img_Bg
            img_out = np.where(condition, img, _imgBg)
        else:
            img_out = np.where(condition, img, img_Bg)
        return img_out
