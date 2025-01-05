"""
This file contains the configuration of Streamlit app Home page and it also serves as the main page of the app.
"""
import Src.scraping.scraper as scraper
import streamlit as st
import sys
import os
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
st.write(os.listdir("/app/Data"))

data_instruments = scraper.load_instruments_data()
st.write("Columns in data_instruments:")
st.write(data_instruments.columns.tolist())