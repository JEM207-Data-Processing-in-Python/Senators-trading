# app.py
import streamlit as st

# Import the pages you want to display
from Pages.home import main as home
from Pages.page1 import page1
from Pages.page2 import page2

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Page 1", "Page 2"])

    # Navigate between pages based on the sidebar selection
    if selection == "Home":
        home()
    elif selection == "Page 1":
        page1()
    elif selection == "Page 2":
        page2()

if __name__ == "__main__":
    main()