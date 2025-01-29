"""
This file contains the configuration of Streamlit app Home page and it also
serves as the main page of the app.
"""
import os

import streamlit as st

from Src.streamlit.home_page import general_information
from Src.scraping.scraper import (Senators_Trading_Updater,
                                  Financial_Instruments_Updater,
                                  Senators_Information_Updater)

# Set the page configuration
st.set_page_config(
    page_title="Home_page",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "### US politicians Trading visualization\n An interactive web"
                 " application visualizing U.S. Senator's financial trading"
                 " activities, analyzing potential insider trading, and offering"
                 " portfolio-based recommendations."
    }
)

# Set Welcome Picture
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(os.path.join("Data", "Profile_picture.jpg"), width=300)

# Title of page
st.title("U.S. Senator's Trading Visualization")

# General Information
unique_politicians, unique_tickers, sum_invested, first_trans, last_update = general_information()

# About the project
st.subheader("About the project")
st.write(
    f"""
    This project aims to visualize U.S. senator's financial trading activities
    based on their financial disclosures. The financial disclosure reports
    provide greater legitimacy for the general public regarding senator's
    investment activities, ensuring that politicians do not create or favor
    laws that could benefit their own investments.

    It features interactive charts of over **{unique_politicians}** politicians
    to explore popular investment sectors, trends of over **{unique_tickers}**
    financial instruments and profit standings among senators which invested
    total of **{sum_invested:,.0f} $** since year **{first_trans}**. It also
    places senators' trading activities in the context of the market and the
    general public. The sub-parts of the project feature:

    - **[Politician Finder](Politician_Finder)**: Provides detailed information
      about individual politicians. It shows general information about the
      politician, their trading activity, exposure to the market, and many
      other interesting insights.

    - **[Instrument Finder](Instrument_Finder)**: Displays how politicians are
      investing in individual financial instruments, along with the performance
      and gains of those instruments.

    - **[Align Your Investment Strategy](Align_Your_Investment_Strategy)**: On
      this page, you can input your investing strategies, and it will show you
      the politicians whose strategies most closely align with yours. This way,
      you can adapt your overall strategy to align with the strategies of
      influential politicians.

    Designed as a Streamlit-based application, this tool offers an engaging way
    to gain insights into senator's trading behaviors and even provides answers
    to well-known questions about insider trading among politicians.
    """
)

# Data
st.subheader("Data Sources")
st.write(
    f"""
    This project draws from multiple credible sources to ensure accurate and
    comprehensive insights into U.S. senator's trading activities and financial
    data. Below is a detailed overview of the data sources that power this
    application:

    - **[TrendSpider](https://trendspider.com/markets/congress-trading)**: One
      of the main sources for our project is TrendSpider, where we scrape
      detailed tables containing the most recent trading activities of U.S.
      senators. These tables are updated daily to reflect disclosures filed by
      the senators themselves. The data provides critical insights into which
      financial instruments are being traded, the transaction types, and the
      overall trends among different senators and political affiliations.

    - **[Yahoo Finance](https://finance.yahoo.com/)**: To complement the trading
      data, we use the Yahoo Finance API to fetch historical and real-time
      market data for financial instruments. This includes stock prices,
      performance trends, and metadata about the financial assets being traded.
      By integrating this data, we can offer in-depth analyses, such as how
      specific trades by senators align with market performance and whether they
      hint at patterns of potential insider trading.

    - **[Wikipedia](https://en.wikipedia.org/)**: To provide background context,
      we leverage the Wikipedia API to gather general information about U.S.
      senators. This includes their profiles, political affiliations, and other
      biographical details, which help enrich the dataset and provide a more
      holistic understanding of the individuals behind the trades. This data is
      particularly useful in identifying patterns related to party lines, voting
      behavior, and trading habits.

    The datasets are not updated automatically, so we provide the option for
    users to update the data using the buttons below. Last data are from
    **{last_update}**. Updating can take a few minutes depending of last update
    date.
    """
)

# Refresh Data
st.subheader("Update Data")
sen_trading, fin_instrument, sen_information = False, False, False

# Columns for buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Update Senators Trading Activity Data'):
        sen_trading = True
with col2:
    if st.button("Update Financial Instruments Data"):
        fin_instrument = True
with col3:
    if st.button("Update Information About Senators"):
        sen_information = True

# Make the update not inside columns
if sen_trading:
    with st.spinner("Updating data..."):
        Senators_Trading_Updater().update_senators_trading()

    st.success("Senator's trading activity data successfully updated!")
    sen_trading = False
elif fin_instrument:
    with st.spinner("Updating data..."):
        Financial_Instruments_Updater().update_financial_instruments()

    st.success("Financial instruments data successfully updated!")
    fin_instrument = False
elif sen_information:
    with st.spinner("Updating data..."):
        Senators_Information_Updater().update_senators_information()

    st.success("Senator's information data successfully updated!")
    sen_information = False
