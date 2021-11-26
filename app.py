import streamlit as st
import numpy as np
import cv2
import dotenv
import detections as dt
from bgRemoval import removeBG
from PIL import Image, ImageEnhance

hide_menu_style = '''
   <style>
      #MainMenu {display: none; }
      footer {visibility: hidden;}
      .css-fk4es0 {display: none;}
      #stStatusWidget {display: none;}
      .css-r698ls {display: none;}
   </style>
'''
st.set_page_config(page_title='Image Procs', layout="wide")
st.markdown(hide_menu_style, unsafe_allow_html=True)

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
         
         st.session_state.enchance_type = ['Original', 'Gray-Scale', 
                                          'Contrast', 'Brightness', 'Blurring', 'Remove-Background']
         st.session_state.enchance = st.sidebar.radio('Enchance Type', st.session_state.enchance_type)

         if 'Original' in st.session_state.enchance:
            st.subheader('Original')
            st.image(img)
            task = ['Original Image', 'Face Detection', 'Smile Detection']
            option_task = st.sidebar.selectbox('Find Features', task)
            if option_task == 'Original Image':
               pass
            elif option_task == 'Face Detection':
               if st.sidebar.button('Detect Faces'):
                  result_img, faces = dt.detect_faces(img)
                  st.subheader('Results')
                  st.image(result_img)
                  if len(faces) > 1:
                     st.success(f'Found {len(faces)} Faces')
                  else:
                     st.success(f'Found {len(faces)} Face')
            elif option_task == 'Smile Detection':
               if st.sidebar.button('Detect Smiles'):
                  result_smile, smiles = dt.detect_smiles(img)
                  st.subheader('Results')
                  st.image(result_smile)
                  if len(smiles) > 0:
                     st.success('Smiling !!!')
                  else:
                     st.error('Not Smiling :(')

         elif 'Gray-Scale' in st.session_state.enchance:
            new_img = np.array(img.convert('RGB'))
            img_cvt = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
            st.subheader('Gray-Scale')
            st.image(img_cvt)

         elif 'Contrast' in st.session_state.enchance:
            c_rate = st.sidebar.slider('Contrast', 0.5, 3.5, step=.5, key='contrast')
            enchancer = ImageEnhance.Contrast(img)
            img_contrast = enchancer.enhance(c_rate)
            st.subheader('Contrast')
            st.image(img_contrast)

         elif 'Brightness' in st.session_state.enchance:
            c_rate = st.sidebar.slider('Brightness', 0.5, 3.5, step=.5, key='brightness')
            enchancer = ImageEnhance.Brightness(img)
            img_brightness = enchancer.enhance(c_rate)
            st.subheader('Brightness')
            st.image(img_brightness)
         
         elif 'Blurring' in st.session_state.enchance:
            blur_rate = st.sidebar.slider('Blurring', 0.5, 3.5, step=.5, key='blurring')
            new_img = np.array(img.convert('RGB'))
            img_blur = cv2.GaussianBlur(new_img, (11, 11), blur_rate)
            st.subheader('Blurring')
            st.image(img_blur)

         else:
            st.subheader('Original')
            st.image(img)
            new_img = np.array(img)
            if st.sidebar.button('Remove Background'):
               imgOut = removeBG(new_img)
               st.subheader('Results')
               st.image(imgOut)

   else:
      st.markdown('''
         ###### Created by __[Lovelyo Yeremia](https://github.com/lovelyoyrmia/)__
         <style>
            a {
               text-decoration: none;
               color: #2235d2;
            }
         </style>
      ''', unsafe_allow_html=True)

if __name__ == '__main__':
   main()
