"""
This file contains the configuration of Streamlit app Align Your Investment Strategy page.
"""
import streamlit as st
import pandas as pd

from Src.visualization.tables import data_for_strategy_align_type, data_for_strategy_align_sector
from Src.streamlit.align_your_investment_strategy import chunk_list, equity_alignment_politician_sector, equity_alignment_politician_instrument, load_and_merge_data, get_unique_sectors_and_instruments
from Src.clustering.cluster import best_alignment

# Set the page configuration
st.set_page_config(
    page_title="Align Your Investment Strategy 📰",
    page_icon="👀",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "### US politicians Trading visualization\n An interactive web application visualizing U.S. Senators' financial trading activities, analyzing potential insider trading, and offering portfolio-based recommendations."
    }
)
st.markdown(
    """
    <style>
        .sector-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 20px;
            padding: 2px;
            box-sizing: border-box;
        }
        .sector-label {
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            height: 45px;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        input {
            width: 90%;
        }
        button[data-baseweb="tab"] {
            font-size: 24px;
            margin: 0;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of page
st.title("Align Your Strategy with Politicians!")

# About
st.write("""
         On this page, you can find your desired investing strategy with politicians who can suggest ways to make investment decisions. This is not financial advice, but rather a fun tool.
         """)

# How it works
st.subheader("How does it work?")

st.write("""
         Insert your desired exposure to individual instruments and sectors. Then, a simple recommendation algorithm will display the politicians with the most similar investment patterns to yours, along with some additional information.
         """)

# Load and merge data using the new function
data_sector, data_instruments = load_and_merge_data()
list_of_unique_sectors, list_of_unique_instruments = get_unique_sectors_and_instruments(data_instruments, data_sector)
strategy_type = data_for_strategy_align_type(data_instruments)
strategy_sector = data_for_strategy_align_sector(data_sector)

# Initialize an empty dictionary for inputs
inputs = {}
inputs_instrument = {}

# The program
st.header("Discover Your Instrument or Equity Strategy Alignment:")

# Create the tabs
tab1, tab2 = st.tabs(["**Instruments alignment**", "**Equity strategy**"])
with tab1:
    st.markdown(f"""
                Politicians in our data invest in the following instruments: **{',  '.join(list_of_unique_instruments)}**.

                Now, you can enter your desirable exposure to the individual instruments based on your portfolio or preferencies.
                The total exposure must sum to 100 % and if you are done press **Submit**.
                """)

    for instrument_chunk in chunk_list(list_of_unique_instruments, 6):
        cols = st.columns(len(instrument_chunk))

        for idx, instrument in enumerate(instrument_chunk):
            with cols[idx]:
                st.markdown('<div class="sector-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="sector-label">{instrument}</div>', unsafe_allow_html=True)
                value = st.number_input("hide", key=f"input_{instrument}", min_value=0, max_value=100, step=1, value=0, format="%d", label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
                inputs_instrument[instrument] = value

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"You assign: {sum(inputs_instrument.values())} / 100")

    with col2:
        disable_submit_button = sum(inputs_instrument.values()) != 100
        submit_button = st.button("SUBMIT", key="Submit_instrument", disabled=disable_submit_button)

    if submit_button:
        # Compute the alignment
        strategy_inserted_instrument = pd.DataFrame(list(inputs_instrument.items()), columns=['quoteType', 'Invested by User'])
        top_5_instrument_strategy = best_alignment(strategy_type, strategy_inserted_instrument, "quoteType")

        st.subheader("Alignment Result")
        st.markdown("---")

        if inputs_instrument["EQUITY"] == 100:
            st.write("There are many politicians with 100 % exposure to the **EQUITY** so the table below may not strictly relevant for you.")
        else:
            st.write(f"Good for you! Your strategy seems to be the most compatible with {top_5_instrument_strategy["Politician"].iloc[0]}")

        st.write(f"""
                 Your investing strategies are **{round(top_5_instrument_strategy["Alignment (%)"].iloc[0], 1)} %** similar. Below you may find the TOP 5 politicians, which whom you have the biggest compliance in your strategy!
                 """)
        st.table(top_5_instrument_strategy)
        st.write("here you can browser the politicians to see the detailed analysis:")

        unique_5_politicians = top_5_instrument_strategy["Politician"].unique().tolist()
        equity_alignment_politician_instrument(unique_5_politicians, list_of_unique_instruments, data_instruments, strategy_inserted_instrument)

    if disable_submit_button:
        st.warning("The sum of inputs is not 100. Please adjust the values.")

with tab2:
    st.markdown(f"""
                Politicians in our data invest in the following sectors: **{',  '.join(list_of_unique_sectors)}**.

                Now, you can enter your desirable exposure to the individual sectors based on your portfolio or preferences. The total exposure must sum to 100 % and if you are done press **Submit**.
                """)

    for sector_chunk in chunk_list(list_of_unique_sectors, 6):
        cols = st.columns(len(sector_chunk))

        for idx, sector in enumerate(sector_chunk):
            with cols[idx]:
                st.markdown('<div class="sector-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="sector-label">{sector}</div>', unsafe_allow_html=True)
                value = st.number_input("hide", key=f"input_{sector}", min_value=0, max_value=100, step=1, value=0, format="%d", label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)
                inputs[sector] = value

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"You assign: {sum(inputs.values())} / 100")

    with col2:
        disable_submit_button = sum(inputs.values()) != 100
        submit_button = st.button("SUBMIT", key="Submit_sector", disabled=disable_submit_button)

    if submit_button:
        if len(inputs) == len(list_of_unique_sectors) and sum(inputs.values()) == 100:
            # Compute the alignment
            strategy_inserted_sector = pd.DataFrame(list(inputs.items()), columns=['sectorKey', 'Invested by User'])
            top_5_sector_strategy = best_alignment(strategy_sector, strategy_inserted_sector, "sectorKey")

            st.subheader("Alignment Result")
            st.markdown("---")
            st.write(f"""
                 Your investing strategies are **{round(top_5_sector_strategy["Alignment (%)"].iloc[0], 1)} %** similar. Below you may find the TOP 5 politicians, which whom you have the biggest compliance in your strategy!
                 """)
            st.table(top_5_sector_strategy)
            st.write("here you can browser the politicians to see the detailed analysis:")

            unique_5_politicians = top_5_sector_strategy["Politician"].unique().tolist()
            equity_alignment_politician_sector(unique_5_politicians, list_of_unique_sectors, data_sector, strategy_inserted_sector)

    if disable_submit_button:
        st.warning("The sum of inputs is not 100. Please adjust the values.")
