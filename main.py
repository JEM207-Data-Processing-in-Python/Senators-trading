"""
This file serves as main entry point for the Streamlit app.
"""
import streamlit as st
import os

# Hide the main.py entry in the sidebar
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul li:nth-child(1) {display: none;}
    </style>
""", unsafe_allow_html=True)

home_page_path = os.path.join("pages", "1_🏠_Home_page.py")
st.switch_page(home_page_path)
