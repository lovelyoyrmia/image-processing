import base64
import streamlit as st

# class FileDownloader(object):
	
# 	def __init__(self, data,filename='myfile',file_ext='jpg'):
# 		super(FileDownloader, self).__init__()
# 		self.data = data
# 		self.filename = filename
# 		self.file_ext = file_ext

# 	def download(self, path_image):
# 		b64 = base64.b64encode(self.data.encode()).decode()
# 		new_filename = "{}_{}_.{}".format(self.filename, path_image,self.file_ext)
# 		st.markdown("#### Download File ###")
# 		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here!!</a>'
# 		st.markdown(href,unsafe_allow_html=True)