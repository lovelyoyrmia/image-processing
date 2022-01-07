import streamlit as st

def imageSt(image):
    st.image(image, use_column_width=True)


def imageSidebar(image):
    st.sidebar.subheader('Original')
    st.sidebar.image(image, use_column_width=True)
