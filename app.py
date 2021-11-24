import streamlit as st
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance


def main():
   # ==== Image Processing ====

   st.title('Image Processing App')
   st.text('Build using streamlit and opencv')

   activities = ['Processing', 'About']
   choice = st.sidebar.selectbox('Select Activity', activities)

   if choice == 'Processing':
      st.subheader('Face Detection')
      image_file = st.file_uploader('Upload Image', type=['png', 'jpg', 'jpeg'])

      if image_file:
         img = Image.open(image_file)
         enchance_type = ['Original', 'Gray-Scale', 'Contrast', 'Brightness', 'Blurring']
         enchance = st.sidebar.radio('Enchance Type', enchance_type)
         
         if enchance == 'Original':
            st.text('Original')
            st.image(img)

         elif enchance == 'Gray-Scale':
            new_img = np.array(img.convert('RGB'))
            img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
            st.image(img_cvt)

         elif enchance == 'Contrast':
            c_rate = st.slider('Contrast', 0.5, 3.5, step=.5)
            enchancer = ImageEnhance.Contrast(img)
            img_contrast = enchancer.enhance(c_rate)
            st.image(img_contrast)

         elif enchance == 'Brightness':
            c_rate = st.slider('Brightness', 0.5, 3.5, step=.5)
            enchancer = ImageEnhance.Brightness(img)
            img_brightness = enchancer.enhance(c_rate)
            st.image(img_brightness)

   else:
      pass

if __name__ == '__main__':
   main()
