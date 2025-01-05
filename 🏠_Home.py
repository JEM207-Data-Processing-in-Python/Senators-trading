"""
This file contains the configuration of Streamlit app Home page and it also serves as the main page of the app.
"""
from Src.scraping.scraper import load_senators_trading
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

import pandas as pd

# File path
file_path = "/app/Data/senators_trading.csv"

# Check if the file exists
if os.path.exists(file_path):
    # Get file size
    file_size = os.path.getsize(file_path)
    file_size_kb = file_size / 1024  # Convert to kilobytes

    # Get file modification time
    mod_time = os.path.getmtime(file_path)
    mod_time_str = pd.to_datetime(mod_time, unit='s')  # Human-readable format

    # Print file information
    st.write("### File Information:")
    st.write(f"**Path:** {file_path}")
    st.write(f"**Size:** {file_size_kb:.2f} KB")
    st.write(f"**Last Modified:** {mod_time_str}")

    # Read and display the CSV
    try:
        data = pd.read_csv(file_path)
        st.write("### Data Preview:")
        st.write(data.head())
        st.write("Data/senators_trading.csv")
        data = pd.read_csv(r"Data/senators_trading.csv")
        st.write(data.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.error(f"The file does not exist at the path: {file_path}")

data_instruments = load_senators_trading()
st.write("Columns in data_instruments:")
st.write(data_instruments.columns.tolist())