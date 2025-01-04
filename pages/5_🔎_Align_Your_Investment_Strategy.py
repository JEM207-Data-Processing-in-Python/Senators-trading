
import streamlit as st
import pandas as pd
from src.visualization.tables import data_for_strategy_align_type, data_for_strategy_align_sector
from src.scraping.scraper import load_senators_trading, load_financial_instruments
from src.streamlit.page_5_functions import best_alignment

#Original data
data_senators = load_senators_trading()
data_instruments = load_financial_instruments()

data_instruments = data_instruments[["Ticker", "quoteType", "currency",
                                     "longName", "shortName", "industry", "sector", "city", 
                                      "country", "industryKey", "industryDisp", "sectorKey", 
                                      "sectorDisp", "longBusinessSummary", "financialCurrency"]]

data = data_senators.merge(data_instruments, how = "left", on = "Ticker")
data = data.fillna("Unknown")

strategy_type = data_for_strategy_align_type(data)
strategy_sector = data_for_strategy_align_sector(data)


# Filter and get the list of unique sectors
list_of_unique_sectors = (
    strategy_sector[strategy_sector["sector"] != "Unknown"]["sector"]
    .dropna()
    .unique()
)

list_of_unique_sectors = list(list_of_unique_sectors)


st.title("Align your strategy!")
st.write("On this page, you may insert your desirable strategy. Insert the desirable exposure to the individual instruments \
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
        height: 120px; /* Standardized height for each container */
        padding: 5px;
        box-sizing: border-box;
    }
    .sector-label {
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        height: 40px; /* Fixed height for labels */
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

# Helper function to chunk the list into groups of 5
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

# Create input fields with a maximum of 5 sectors per row
st.write("Enter values for each sector (must sum to 100):")
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
if st.button("Submit"):
    if len(inputs) == len(list_of_unique_sectors) and sum(inputs.values()) == 100:
        st.success(f"All inputs are valid. Proceed to Investment alignment")

        strategy_inserted_sector = pd.DataFrame(list(inputs.items()), columns=['sector', 'Invested by User'])

        top_5_sector_strategy = best_alignment(strategy_sector, strategy_inserted_sector)

        st.table(top_5_sector_strategy)

    elif len(inputs) == len(list_of_unique_sectors):
        st.warning(f"Ensure the sum of inputs is equal to 100 (current sum: {sum(inputs.values())}/100).")
    else:
        st.warning("Your inputs are invalid.")




