"""
This file contains the configuration of Streamlit app Politician Finder page.
"""
import streamlit as st
from .src.visualization.graphs import pie_chart_advanced, grouping_for_graph, five_days_graph, grouping_for_barchart
from .src.scraping.scraper import load_senators_trading, load_financial_instruments
from .src.streamlit.page_1_data_gather import *

#Original data
data_senators = load_senators_trading()
data_instruments = load_financial_instruments()

data_instruments = data_instruments[["Ticker", "quoteType", "currency",
                                     "longName", "shortName", "industry", "sector", "city", 
                                      "country", "industryKey", "industryDisp", "sectorKey", 
                                      "sectorDisp", "longBusinessSummary", "financialCurrency"]]

data = data_senators.merge(data_instruments, how = "left", on = "Ticker")
data = data.fillna("Unknown")

#Lists for Interactive Buttons:
list_of_politicians = data.Politician.unique()
list_of_politicians.sort()

# Set the page configuration
st.set_page_config(
    page_title="Politician Finder 👨‍💼",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "### US politicians Trading visualization\n An interactive web application visualizing U.S. Senators' financial trading activities, analyzing potential insider trading, and offering portfolio-based recommendations."
    }
)

#Page definition
st.title("Get to know a politician 👨‍💼🏛️")
st.write("On this page, you may browse through the investing history of the US politicians. \
            You may find there their trading activity, exposure to the market and many interesting information.")
selected_politician = st.selectbox(
                            "Select a politician:",
                            options=list_of_politicians)

st.title(selected_politician)

#FIRST SECTION
st.subheader("General information")

#Get information for interactive text
party_politician_value = party_politician(data, selected_politician)
chamber_politician_value = chmaber_politician(data, selected_politician)
first_trade_politician_value = first_trade_politician(data, selected_politician)
last_trade_politician_value = last_trade_politician(data, selected_politician)
total_invested_politician_value = total_invested_politician(data, selected_politician)
total_sold_politician_value = total_sold_politician(data, selected_politician)                                 


#Page content
st.write(f"You are looking at the information about {selected_politician}. They are a member of {party_politician_value}.\
                {selected_politician} is present in the {chamber_politician_value}. Their first documenteed transaction happend on {first_trade_politician_value}. \
            Since then, {selected_politician} has purchased instruments in total amount of {total_invested_politician_value} USD and has sold instruments \
            in total value of {total_sold_politician_value} USD. Their last documented transaction happened on {last_trade_politician_value}.")

    # Button to show the bar chart (Total Investment per Month)
st.write(f"To display the history of trading activity of {selected_politician}, select one of the tabs. Barchart displays their trading activity\
            summarized by month. Linechart displays the trading activity continuously:")

tab1, tab2 = st.tabs(["📊 BARCHART", "📈 LINECHART"])

with tab1:
    try:
        barchart_invested_in_time = grouping_for_barchart("Politician", selected_politician, data)
        st.plotly_chart(barchart_invested_in_time, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")

with tab2:
    try:
        chart_invested_in_time = grouping_for_graph("Politician", selected_politician, data)
        st.plotly_chart(chart_invested_in_time, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")


#SECOND SECTION
st.subheader("Exposure to the market")

#GET the information for interactive text
message_1 = most_trade_type_politician(data, selected_politician)
message_2 = most_traded_volume_politician(data, selected_politician)
message_3 = most_traded_sector_politician(data, selected_politician)
message_4 = most_sold_sector_politician(data, selected_politician)

st.write(f"{message_1} {message_2} {message_3} {message_4}")

# Charts
st.write("Select whether you want to see the graphs for Purchases or Sales:")

# Create tabs for "Purchase" and "Sale"
tabs = st.tabs(["Purchase 📈", "Sale 📉"])

with tabs[0]:  # Purchase tab
    if message_3 == "They has not invested in EQUITY either.":
        st.write("There are no documented Purchases.")
    else:
        purchase = "Purchase"
        col1, col2 = st.columns(2)
        with col1:
            try:
                chart_pie_chart_exposure_1 = pie_chart_advanced(data, purchase, "quoteType", selected_politician)
                st.plotly_chart(chart_pie_chart_exposure_1, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

        with col2:
            try:
                chart_pie_chart_exposure_2 = pie_chart_advanced(data, purchase, "sector", selected_politician)
                st.plotly_chart(chart_pie_chart_exposure_2, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

with tabs[1]:  # Sale tab
    if message_4 == "They did not perform any sales of EQUITY during the documented time period.":
        st.write("There are no documented Sales.")
    else:
        purchase = "Sale"
        col1, col2 = st.columns(2)
        with col1:
            try:
                chart_pie_chart_exposure_1 = pie_chart_advanced(data, purchase, "quoteType", selected_politician)
                st.plotly_chart(chart_pie_chart_exposure_1, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

        with col2:
            try:
                chart_pie_chart_exposure_2 = pie_chart_advanced(data, purchase, "sector", selected_politician)
                st.plotly_chart(chart_pie_chart_exposure_2, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")


# THIRD SECTION
st.subheader("Main Individual Investments")
st.write(f"Here you can see {selected_politician}'s five most purchased and sold instruments per type.")
st.write("Firstly, select whether you are interested in Purchases or Sales:")

# Ensure session state for `purchase_section_three` exists
if "purchase_section_three" not in st.session_state:
    st.session_state.purchase_section_three = "Purchase"

# Create tabs for Purchases and Sales
tab_purchase, tab_sale = st.tabs(["Purchases 📈", "Sales 📉"])

with tab_purchase:
    # Check if there are any documented Purchases
    if "Purchase" not in data[data["Politician"] == selected_politician].Transaction.unique():
        st.write("There are no documented Purchases.")
    else:
        st.session_state.purchase_section_three = "Purchase"

        # Dropdown for Purchases
        list_of_types_of_instruments = list(
            map(
                str,
                data[
                    (data["Politician"] == selected_politician) & 
                    (data["Transaction"] == "Purchase")
                ].quoteType.unique()
            )
        )
        list_of_types_of_instruments.sort()

        selected_type_of_instrument_section_three = st.selectbox(
            "Select an instrument:",
            options=list_of_types_of_instruments,
        )

        # Call the function for Purchases
        section_three_purchase_table(
            data, list_of_types_of_instruments, selected_politician, 
            "Purchase", selected_type_of_instrument_section_three
        )

with tab_sale:
    # Check if there are any documented Sales
    if "Sale" not in data[data["Politician"] == selected_politician].Transaction.unique():
        st.write("There are no documented Sales.")
    else:
        st.session_state.purchase_section_three = "Sale"

        # Dropdown for Sales
        list_of_types_of_instruments = list(
            map(
                str,
                data[
                    (data["Politician"] == selected_politician) & 
                    (data["Transaction"] == "Sale")
                ].quoteType.unique()
            )
        )
        list_of_types_of_instruments.sort()

        selected_type_of_instrument_section_three = st.selectbox(
            "Select an instrument:",
            options=list_of_types_of_instruments,
            key="Sale"
        )

        # Call the function for Sales
        section_three_purchase_table(
            data, list_of_types_of_instruments, selected_politician, 
            "Sale", selected_type_of_instrument_section_three
        )


#FOURTH SECTION
st.subheader("Most active days")

most_active_purchase_value = most_active_purchase(data, selected_politician)
most_active_sell_value = most_active_sell(data, selected_politician)

st.write(f"{most_active_purchase_value} \n \n {most_active_sell_value}")

try:
    barchart_five_days = five_days_graph(data, selected_politician)
    st.plotly_chart(barchart_five_days, use_container_width=True)
except Exception as e:
    st.error(f"Error generating chart: {e}")
