import streamlit as st
import numpy as np
import cv2
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
                  result_smile = dt.detect_smiles(img)
                  st.subheader('Results')
                  st.image(result_smile)
                  

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
         ### Follow me on \n
        
         <div class='icon-container'>
            <a href='https://github.com/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><g fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385c.6.105.825-.255.825-.57c0-.285-.015-1.23-.015-2.235c-3.015.555-3.795-.735-4.035-1.41c-.135-.345-.72-1.41-1.23-1.695c-.42-.225-1.02-.78-.015-.795c.945-.015 1.62.87 1.845 1.23c1.08 1.815 2.805 1.305 3.495.99c.105-.78.42-1.305.765-1.605c-2.67-.3-5.46-1.335-5.46-5.925c0-1.305.465-2.385 1.23-3.225c-.12-.3-.54-1.53.12-3.18c0 0 1.005-.315 3.3 1.23c.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23c.66 1.65.24 2.88.12 3.18c.765.84 1.23 1.905 1.23 3.225c0 4.605-2.805 5.625-5.475 5.925c.435.375.81 1.095.81 2.22c0 1.605-.015 2.895-.015 3.3c0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" fill="currentColor"/></g>
            </svg></a>
            <a href='https://www.instagram.com/lovelyoyrmia/' target='_blank' rel='noopener noreferrer'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><g fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.465 1.066C8.638 1.012 9.012 1 12 1c2.988 0 3.362.013 4.534.066c1.172.053 1.972.24 2.672.511c.733.277 1.398.71 1.948 1.27c.56.549.992 1.213 1.268 1.947c.272.7.458 1.5.512 2.67C22.988 8.639 23 9.013 23 12c0 2.988-.013 3.362-.066 4.535c-.053 1.17-.24 1.97-.512 2.67a5.396 5.396 0 0 1-1.268 1.949c-.55.56-1.215.992-1.948 1.268c-.7.272-1.5.458-2.67.512c-1.174.054-1.548.066-4.536.066c-2.988 0-3.362-.013-4.535-.066c-1.17-.053-1.97-.24-2.67-.512a5.397 5.397 0 0 1-1.949-1.268a5.392 5.392 0 0 1-1.269-1.948c-.271-.7-.457-1.5-.511-2.67C1.012 15.361 1 14.987 1 12c0-2.988.013-3.362.066-4.534c.053-1.172.24-1.972.511-2.672a5.396 5.396 0 0 1 1.27-1.948a5.392 5.392 0 0 1 1.947-1.269c.7-.271 1.5-.457 2.67-.511zm8.98 1.98c-1.16-.053-1.508-.064-4.445-.064c-2.937 0-3.285.011-4.445.064c-1.073.049-1.655.228-2.043.379c-.513.2-.88.437-1.265.822a3.412 3.412 0 0 0-.822 1.265c-.151.388-.33.97-.379 2.043c-.053 1.16-.064 1.508-.064 4.445c0 2.937.011 3.285.064 4.445c.049 1.073.228 1.655.379 2.043c.176.477.457.91.822 1.265c.355.365.788.646 1.265.822c.388.151.97.33 2.043.379c1.16.053 1.507.064 4.445.064c2.938 0 3.285-.011 4.445-.064c1.073-.049 1.655-.228 2.043-.379c.513-.2.88-.437 1.265-.822c.365-.355.646-.788.822-1.265c.151-.388.33-.97.379-2.043c.053-1.16.064-1.508.064-4.445c0-2.937-.011-3.285-.064-4.445c-.049-1.073-.228-1.655-.379-2.043c-.2-.513-.437-.88-.822-1.265a3.413 3.413 0 0 0-1.265-.822c-.388-.151-.97-.33-2.043-.379zm-5.85 12.345a3.669 3.669 0 0 0 4-5.986a3.67 3.67 0 1 0-4 5.986zM8.002 8.002a5.654 5.654 0 1 1 7.996 7.996a5.654 5.654 0 0 1-7.996-7.996zm10.906-.814a1.337 1.337 0 1 0-1.89-1.89a1.337 1.337 0 0 0 1.89 1.89z" fill="currentColor"/></g>
            </svg></a>
            <a href='https://www.linkedin.com/in/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><g fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1 2.838A1.838 1.838 0 0 1 2.838 1H21.16A1.837 1.837 0 0 1 23 2.838V21.16A1.838 1.838 0 0 1 21.161 23H2.838A1.838 1.838 0 0 1 1 21.161V2.838zm8.708 6.55h2.979v1.496c.43-.86 1.53-1.634 3.183-1.634c3.169 0 3.92 1.713 3.92 4.856v5.822h-3.207v-5.106c0-1.79-.43-2.8-1.522-2.8c-1.515 0-2.145 1.089-2.145 2.8v5.106H9.708V9.388zm-5.5 10.403h3.208V9.25H4.208v10.54zM7.875 5.812a2.063 2.063 0 1 1-4.125 0a2.063 2.063 0 0 1 4.125 0z" fill="currentColor"/></g>
            </svg></a>
         </div>
         <h5>Created by Lovelyo Yeremia</h5>
         <style>
            .icon-container a {
               text-decoration: none;
               color: #2235d2;
               font-size: 2rem;
            }
            .icon-container {
               display: flex;
               width: 30%;
               justify-content: space-between;
            }
            .icon-container a:hover {
               color: grey;
            }
            h5 {
               margin-top: 2rem;
            }
         </style>
      ''', unsafe_allow_html=True)

if __name__ == '__main__':
   main()
