"""
This file serves as main entry point for the Streamlit app.
"""
import streamlit as st

# Hide the main.py entry in the sidebar
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul li:nth-child(1) {display: none;}
    </style>
""", unsafe_allow_html=True)

st.switch_page("Pages/1_🏠_Home_Page.py")
