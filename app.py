from attr.setters import convert
import streamlit as st
import numpy as np
import cv2
import os
import random
import requests
import base64
import dotenv
import detections as dt
from PIL import Image, ImageEnhance

path_image = str(random.randint(0, 100000))

@st.cache()
def load_image(image_file):
   img = Image.open(image_file)
   return img

def main():
   dotenv.load_dotenv()
   # ==== Image Processing ====
   st.title('Image Processing App')
   st.text('Build using streamlit and opencv')

   activities = ['Processing', 'About']
   choice = st.sidebar.selectbox('Select Activity', activities)

   if choice == 'Processing':
      # st.subheader('Face Detection')
      image_file = st.file_uploader('Upload Image', type=['png', 'jpg', 'jpeg'])
      # image_decode = base64.b64encode(image_file.read()).decode('utf-8')

      if image_file:
         
         img = load_image(image_file)
         image_array = np.array(img)

         # TODO: I'll be back later

         # response = requests.post(
         #    'https://api.remove.bg/v1.0/removebg',
         #    files={'image_file': open('vio.jpg', 'rb')},
         #    data={
         #       'size': 'auto' 
         #    },
         #    headers={'X-Api-Key': os.environ.get('X_API_KEY')}
         # )
         
         enchance_type = ['Original', 'Gray-Scale', 'Contrast', 'Brightness', 'Blurring', 'Remove-Background']
         enchance = st.sidebar.radio('Enchance Type', enchance_type)

         if enchance == 'Original':
            st.text('Original')
            st.image(img)
            task = ['Original Image', 'Face Detection', 'Body Detection', 'Smile Detection']
            option_task = st.sidebar.selectbox('Find Features', task)
            if option_task == 'Original Image':
               pass
            elif option_task == 'Face Detection':
               if st.button('Detect Faces'):
                  result_img, faces = dt.detect_faces(img)
                  st.image(result_img)
                  if len(faces) > 1:
                     st.success(f'Found {len(faces)} Faces')
                  else:
                     st.success(f'Found {len(faces)} Face')
            elif option_task == 'Body Detection':
               pass
            elif option_task == 'Smile Detection':
               if st.button('Detect Smiles'):
                  result_smile, smiles = dt.detect_smiles(img)
                  st.image(result_smile)
                  if len(smiles) > 0:
                     st.success('Smiling !!!')
                  else:
                     st.error('Not Smiling :(')

         elif enchance == 'Gray-Scale':
            new_img = np.array(img.convert('RGB'))
            img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
            st.image(img_cvt)

         elif enchance == 'Contrast':
            c_rate = st.sidebar.slider('Contrast', 0.5, 3.5, step=.5)
            enchancer = ImageEnhance.Contrast(img)
            img_contrast = enchancer.enhance(c_rate)
            st.subheader('Contrast')
            st.image(img_contrast)

         elif enchance == 'Brightness':
            c_rate = st.slider('Brightness', 0.5, 3.5, step=.5)
            enchancer = ImageEnhance.Brightness(img)
            img_brightness = enchancer.enhance(c_rate)
            st.image(img_brightness)
         
         elif enchance == 'Blurring':
            blur_rate = st.slider('Brightness', 0.5, 3.5, step=.5)
            new_img = np.array(img.convert('RGB'))
            img_blur = cv2.GaussianBlur(new_img, (11, 11), blur_rate)
            st.image(img_blur)

         else:
            st.subheader('Original')
            st.image(img)
            # try:
            #    if response.status_code == requests.codes.ok :
            #       img_rmove = response.content
            #       st.image(img_rmove)
            #    else:
            #       print(response.status_code)
            # except Exception as err:
            #    print(err)

   else:
      pass

if __name__ == '__main__':
   main()
