"""
This file contains the configuration of Streamlit app Home page and it also serves as the main page of the app.
"""

import streamlit as st

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

st.title("Main App page")
st.write("Navigate to other pages!")
