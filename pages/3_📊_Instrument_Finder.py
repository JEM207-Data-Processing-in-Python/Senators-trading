"""
This file contains the configuration of Streamlit app Instrument Finder page.
"""
import streamlit as st

from Src.streamlit.instrument_finder import instrument_information, transform_data, process_politician_data
from Src.visualization.graphs_istrument_finder import PoliticianGraph

# Set the page configuration
st.set_page_config(
    page_title="Instrument Finder 📊",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "### US politicians Trading visualization\n An interactive web"
                 " application visualizing U.S. Senators' financial trading"
                 " activities, analyzing potential insider trading, and offering"
                 " portfolio-based recommendations."
    }
)
st.markdown(
    """
    <style>
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
st.title("Trades visualization 📊")

# About the page
st.subheader("About the page")
st.write(
    """
    On this page, you can explore the trading activity of U.S. politicians from the Senate and House
    for invidual instrument. You can compare their trades to overall market performance and gain
    insights into their market exposure. Detailed information about the company and current revenue
    of the trade. We use S&P 500 as a benchmark to compare the performance of the instrument.
    """
)

# data transformation
list_of_instruments, data = transform_data()

# Dropdown for selecting a instrument
st.subheader("Select the financial instrument you are interested in:")
selected_instrument = st.selectbox("hide", options=list_of_instruments, label_visibility="collapsed")
st.markdown("---")

# Display information about the selected instrument
st.header(selected_instrument)
st.subheader("About the Instrument")
st.write(instrument_information(data, selected_instrument))

# Filter data for selected politician
instrument_data = data[data['Name'] == selected_instrument]
list_of_politicians = instrument_data['Politician'].unique().tolist()

# Create tabs for each instrument
tabs = st.tabs(list_of_politicians)
for i, politician in enumerate(list_of_politicians):
    with tabs[i]:
        # Politician data processing
        st.subheader(f"{politician} Trades")

        # Status of the trades for the selected politician
        data_display, weighted_profit, politician_data = process_politician_data(instrument_data, politician)
        st.dataframe(data_display, use_container_width=True, hide_index=True)
        st.write(f"{politician} has made a total profit of **{politician_data['Profit'].sum()} $** from trading "
                 f"**{selected_instrument}** with an average gain of **{weighted_profit} %**. However, the S&P 500 "
                 f"has gained an average of **{politician_data['S&P 500'].mean():.2f}** % during the same period.")

        if weighted_profit > politician_data['S&P 500'].mean():
            st.write(f"{politician} has outperformed the S&P 500. So the Politician can use some advantage of "
                     "insider trading information.")
        elif weighted_profit < politician_data['S&P 500'].mean():
            st.write(f"**{politician}** has underperformed the S&P 500. So the Politician probably do not have "
                     "insider trading information.")

        # Graph generation
        graph = PoliticianGraph(politician_data, selected_instrument)
        fig = graph.generate_graph()
        st.plotly_chart(fig)
