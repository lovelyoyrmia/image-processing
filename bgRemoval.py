import cv2
import mediapipe as mp
import numpy as np


mpDraw = mp.solutions.drawing_utils
mpSegment = mp.solutions.selfie_segmentation
selfieSegmentation = mpSegment.SelfieSegmentation()

def removeBG(img, imgBg=(255, 255, 255), threshold=0.1):
   global mpDraw, mpSegment, selfieSegmentation
   imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = selfieSegmentation.process(imgRGB)
   condition = np.stack(
      (results.segmentation_mask,) * 3, axis=-1) > threshold
   if isinstance(imgBg, tuple):
      _imgBg = np.zeros(img.shape, dtype=np.uint8)
      _imgBg[:] = imgBg
      imgOut = np.where(condition, img, _imgBg)
   else:
      imgOut = np.where(condition, img, imgBg)
   return imgOut
