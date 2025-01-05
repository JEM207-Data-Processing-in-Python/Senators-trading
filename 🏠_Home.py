"""
This file contains the configuration of Streamlit app Home page and it also serves as the main page of the app.
"""

import streamlit as st
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
# Set the page configuration
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "### US politicians Trading visualization\n An interactive web application visualizing U.S. Senators' financial trading activities, analyzing potential insider trading, and offering portfolio-based recommendations.\n\n *Made by Dario Mikuš and Michal Smieško*"
    }
)

st.title("Main App")
st.write("Navigate to other pages!")
st.write("Python Path:")
st.write(sys.path)

st.write("App Directory Contents:")
st.write(os.listdir("/app"))

# List the contents of the src directory
st.write("SRC Directory Contents:")
st.write(os.listdir("/app/Src"))