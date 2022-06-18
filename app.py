import streamlit as st
from _utils import *
from PIL import Image


def main():
    image_logo = Image.open("assets/logo_app.png")
    st.set_page_config(page_title="Image Procs", page_icon=image_logo, layout="wide")
    hide_menu_style = """
    <style>
        #MainMenu {display: none; }
        footer {visibility: hidden;}
        .css-fk4es0 {display: none;}
        #stStatusWidget {display: none;}
        .css-r698ls {display: none;}
    </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # ==== Image Processing ====
    st.title("Image Processing App")
    st.text("Build using Computer Vision and Artificial Intelligence")

    activities = [
        "Welcome",
        "Processing",
        "Computer Vision Features",
        "Get In Touch",
        "About",
    ]
    navigation = st.sidebar.selectbox("Select Activity", activities)
    nav = Navigation(st)

    # ALL VARIABLES IMAGE

    # === Welcome Page ===
    if navigation == "Welcome":
        nav.welcome()

    # === Processing Page ===
    elif navigation == "Processing":
        processing()

    elif navigation == "Computer Vision Features":
        computerVisionFeatures()

    # === Get In Touch Page ===
    elif navigation == "Get In Touch":
        nav.contact()

    # === About Page ===
    else:
        nav.aboutPage()


if __name__ == "__main__":
    main()
