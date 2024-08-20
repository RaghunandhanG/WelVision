
import streamlit as st
import cv2
import torch
from PIL import Image
import numpy as np
import os
import subprocess
import shutil
import yaml
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from realtime import get_path

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Authentication widget
name, authentication_status, username = authenticator.login('Login', 'main')  # Correctly place in the main section

if authentication_status:
    st.title('Settings')
    directory = r"C:\Users\Raghunandhan G\Desktop\WelVision\models"
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    

    option = st.selectbox(
        "Select the Model",
        files,
    )
    option = directory + "\\" + option
    
    st.session_state.selected_option = option

    st.write("You selected:", option)
    get_path(option)
    
    # authenticator.logout('Logout', 'main')
    
    
elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
