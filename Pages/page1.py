import streamlit as st
from Src.visualization.graphs import pie_chart_chamber

# Page1.py
import streamlit as st

def page1():
    st.title("Page 1")
    st.write("This is page 1 of the app.")
    st.plotly_chart(pie_chart_chamber())

if __name__ == "__main__":
    page1()