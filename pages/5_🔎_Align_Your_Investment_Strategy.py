
import streamlit as st
import pandas as pd
from Src.visualization.tables import data_for_strategy_align_type, data_for_strategy_align_sector
from Src.scraping.scraper import load_senators_trading, load_financial_instruments
from Src.streamlit.page_5_functions import best_alignment_sector, equity_alignment_politician_sector, best_alignment_instrument, equity_alignment_politician_instrument

#Original data
data_senators = load_senators_trading()
data_instruments = load_financial_instruments()

data_instruments = data_instruments[["Ticker", "quoteType", "currency",
                                     "longName", "shortName", "industry", "sector", "city", 
                                      "country", "industryKey", "industryDisp", "sectorKey", 
                                      "sectorDisp", "longBusinessSummary", "financialCurrency"]]

data = data_senators.merge(data_instruments, how = "left", on = "Ticker")
data = data.fillna("Unknown")
data_sector = data[data["sector"] != "Unknown"]
data_instruments = data[data["quoteType"] != "Unknown"]

strategy_type = data_for_strategy_align_type(data_instruments)
strategy_sector = data_for_strategy_align_sector(data_sector)


# Filter and get the list of unique sectors
list_of_unique_sectors = (
    strategy_sector[strategy_sector["sector"] != "Unknown"]["sector"]
    .dropna()
    .unique()
)

list_of_unique_sectors = list(list_of_unique_sectors)


list_of_unique_instruments = (
    strategy_type[strategy_type["quoteType"] != "Unknown"]["quoteType"]
    .dropna()
    .unique()
)

list_of_unique_instruments = list(list_of_unique_instruments)


st.title("Align your strategy!")
st.write("On this page, you may insert your desirable strategy... Insert the desirable exposure to the individual instruments \
         and to the individual sectors. The program then displays the politicians with the most similar strategy to yours with additional information \
         so you may adapt your overall strategy.")
# Apply custom CSS for alignment and handling long text
st.markdown(
    """
    <style>
    .sector-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 20px; /* Standardized height for each container */
        padding: 2px;
        box-sizing: border-box;
    }
    .sector-label {
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        height: 20px; /* Fixed height for labels */
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    input {
        width: 90%; /* Make input boxes more compact */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize an empty dictionary for inputs
inputs = {}
inputs_instrument = {}

# Helper function to chunk the list into groups of 5
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

# Create input fields with a maximum of 5 sectors per row
st.subheader("Align either Instrument or Equity strategy:")

tab1, tab2 = st.tabs(["INSTRUMENTS", "EQUITY"])

with tab1:
    st.markdown("Politicians invest in the following instruments... Now, you may enter your desirable exposure to the individual instruments. \
                Total exposure must sum to 100 (%). \
                Enter only numbers without any special symbols. If you do not want to invest in some instrument, insert 0. If your total exposure is 100 and you are \
                satisfied with your allocation, press 'SUBMIT' at the bottom and see your final compliances.")
    for instrument_chunk in chunk_list(list_of_unique_instruments, 6):
        cols = st.columns(len(instrument_chunk))
        for idx, instrument in enumerate(instrument_chunk):
            with cols[idx]:
                st.markdown('<div class="sector-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="sector-label">{instrument}</div>', unsafe_allow_html=True)
                value = st.text_input("", key=f"input_{instrument}")
                st.markdown('</div>', unsafe_allow_html=True)
                if value:
                    try:
                        number = float(value)
                        if 0 <= number <= 100:
                            inputs_instrument[instrument] = number
                        else:
                            st.error(f"Value for {instrument} must be between 0 and 100.")
                    except ValueError:
                        st.error(f"Value for {instrument} must be a number.")

    # Validate inputs and ensure the sum is 100               
    st.markdown(f"Input total: {round(sum(inputs_instrument.values()),2)} / 100")
    if st.button("SUBMIT", key = "Submit_instrument"):
        if len(inputs_instrument) == len(list_of_unique_instruments) and sum(inputs_instrument.values()) == 100:
            
            st.markdown("---")
            strategy_inserted_instrument = pd.DataFrame(list(inputs_instrument.items()), columns=['quoteType', 'Invested by User'])

            top_5_instrument_strategy = best_alignment_instrument(strategy_type, strategy_inserted_instrument)
            
            if inputs_instrument["EQUITY"] == 100:
                st.subheader("There are many politicians with 100% exposure to the EQUITY and the table below is not relevant.")
            else:
                st.subheader(f"CONGRATS! Your strategy is the most compatible with {top_5_instrument_strategy["Politician"].iloc[0]}")
            st.write(f"Your strategies are compatible on {round(top_5_instrument_strategy["Alignment (%)"].iloc[0],1)} %")
            st.write("Below you may find the TOP 5 politicians, which whom you have the biggest compliance in strategy!")

            st.table(top_5_instrument_strategy)

            unique_5_politicians = top_5_instrument_strategy["Politician"].unique().tolist()

            st.write("Select one of the politicians to see the detailed analysis:")

            equity_alignment_politician_instrument(unique_5_politicians, list_of_unique_instruments, data_instruments, strategy_inserted_instrument)



with tab2:
    st.markdown("Politicians invest in the following sectors. Now, you may enter your desirable exposure to the individual sectors. Total exposure must sum to 100 (%). \
                Enter only numbers without any special symbols. If you do not want to invest in some sector, insert 0. If your total exposure is 100 and you are \
                satisfied with your allocation, press 'SUBMIT' at the bottom and see your final compliances.")

    for sector_chunk in chunk_list(list_of_unique_sectors, 6):
        cols = st.columns(len(sector_chunk))
        for idx, sector in enumerate(sector_chunk):
            with cols[idx]:
                st.markdown('<div class="sector-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="sector-label">{sector}</div>', unsafe_allow_html=True)
                value = st.text_input("", key=f"input_{sector}")
                st.markdown('</div>', unsafe_allow_html=True)
                if value:
                    try:
                        number = float(value)
                        if 0 <= number <= 100:
                            inputs[sector] = number
                        else:
                            st.error(f"Value for {sector} must be between 0 and 100.")
                    except ValueError:
                        st.error(f"Value for {sector} must be a number.")

    # Validate inputs and ensure the sum is 100
    st.markdown(f"Input total: {round(sum(inputs.values()),0)} / 100")
    if st.button("SUBMIT", key = "Submit_sector"):
        if len(inputs) == len(list_of_unique_sectors) and sum(inputs.values()) == 100:
            
            st.markdown("---")
            strategy_inserted_sector = pd.DataFrame(list(inputs.items()), columns=['sector', 'Invested by User'])
            top_5_sector_strategy = best_alignment_sector(strategy_sector, strategy_inserted_sector)
            
            st.subheader(f"CONGRATS! Your strategy is the most compatible with {top_5_sector_strategy["Politician"].iloc[0]}")
            st.write(f"Your strategies are compatible on {round(top_5_sector_strategy["Alignment (%)"].iloc[0],1)} %")
            st.write("Below you may find the TOP 5 politicians, which whom you have the biggest compliance in strategy!")


            st.table(top_5_sector_strategy)

            unique_5_politicians = top_5_sector_strategy["Politician"].unique().tolist()

            st.write("Select one of the politicians to see the detailed analysis:")

            equity_alignment_politician_sector(unique_5_politicians, list_of_unique_sectors, data_sector, strategy_inserted_sector)

            
        elif len(inputs) == len(list_of_unique_sectors):
            st.warning(f"Ensure the sum of inputs is equal to 100 (current sum: {sum(inputs.values())}/100).")
        else:
            st.warning("Your inputs are invalid.")




