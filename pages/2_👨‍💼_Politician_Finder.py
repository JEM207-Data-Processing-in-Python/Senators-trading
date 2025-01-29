"""
This file contains the configuration of Streamlit app Politician Finder page.
"""
import streamlit as st

from Src.scraping.scraper import DataLoader
from Src.visualization.graphs_politician_finder import Politician_Data_Visualizer
from Src.streamlit.politician_finder_1 import (
    party_politician, first_trade_politician, last_trade_politician,
    total_invested_politician, total_sold_politician
)
from Src.streamlit.politician_finder_2 import (
    most_trade_type_politician, most_traded_volume_politician,
    most_traded_sector_politician, most_sold_sector_politician
)
from Src.streamlit.politician_finder_3 import (
    most_active_purchase, most_active_sell, section_three_purchase_table,
    chamber_politician, wikipedia_information
)

# Set the page configuration
st.set_page_config(
    page_title="Politician Finder 👨‍💼",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': (
            "### US politicians Trading visualization\n An interactive web "
            "application visualizing U.S. Senators' financial trading activities, "
            "analyzing potential insider trading, and offering portfolio-based "
            "recommendations."
        )
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
st.title("Get to know a U.S. politician 👨‍💼🏛️")

# About the page
st.subheader("About the page")
st.write("""
    On this page, you can explore the investment history of U.S. politicians from
    the Senate and House. You’ll find detailed insights into their trading activity,
    market exposure, and other fascinating information about their investment
    disclosures.
""")

# Original data
data_senators = DataLoader().load_senators_trading()
data_instruments = DataLoader().load_financial_instruments()

data_instruments = data_instruments[[
    "Ticker", "quoteType", "longName", "shortName", "city", "country",
    "industryKey", "sectorKey", "longBusinessSummary", "financialCurrency",
    "currency"
]]

data = data_senators.merge(data_instruments, how="left", on="Ticker")
data = data.fillna("Unknown")

# Lists for Interactive Buttons:
list_of_politicians = data.Politician.unique()
list_of_politicians.sort()

# Dropdown for selecting a politician
st.subheader("Select the politician you want to learn more about:")
selected_politician = st.selectbox("hide", options=list_of_politicians, label_visibility="collapsed")
st.markdown("---")
st.header(selected_politician)

# General information
st.subheader("General information")

# Get information for interactive text
party_politician_value = party_politician(data, selected_politician)
chamber_politician_value = chamber_politician(data, selected_politician)
first_trade_politician_value = first_trade_politician(data, selected_politician)
last_trade_politician_value = last_trade_politician(data, selected_politician)
total_invested_politician_value = total_invested_politician(data, selected_politician)
total_sold_politician_value = total_sold_politician(data, selected_politician)
information, url, picture = wikipedia_information(selected_politician)

content = (
    f"You are looking at the information about **{selected_politician}**, a member "
    f"of the **{party_politician_value}** in the **{chamber_politician_value}**. "
    f"Their first documented transaction occurred on **{first_trade_politician_value}**. "
    f"Since then, **{selected_politician}** has purchased instruments totaling "
    f"**{total_invested_politician_value} USD** and sold instruments totaling "
    f"**{total_sold_politician_value} USD**. Their last documented transaction "
    f"occurred on **{last_trade_politician_value}**."
)
if information is not None:
    content += f"\n{information}"

if url is not None:
    content += f"\n\n[Read more on Wikipedia]({url})"

# Display the information
if picture is not None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(content)
    with col2:
        st.image(picture, use_container_width=True)
else:
    st.write(content)


# General information
st.subheader("History of trading activity")
st.write(f"""
    Explore the trading history of {selected_politician} through the tabs
    provided. The Barchart offers a monthly summary of their trading activity,
    highlighting trends in purchases and sales, while the Linechart presents a
    continuous timeline of transactions for a detailed view of their trading
    patterns.
""")

# Graphs
tab1, tab2 = st.tabs(["📊 BARCHART", "📈 LINECHART"])
with tab1:
    try:
        visualizer = Politician_Data_Visualizer(data)
        barchart_invested_time = visualizer.grouping_for_barchart("Politician", selected_politician)
        st.plotly_chart(barchart_invested_time, use_container_width=True, use_svg=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")

with tab2:
    try:
        visualizer = Politician_Data_Visualizer(data)
        chart_invested_in_time = visualizer.grouping_for_graph("Politician", selected_politician)
        st.plotly_chart(chart_invested_in_time, use_container_width=True, use_svg=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")


# Exposure to the market
st.subheader("Exposure to the market")

# Get information for interactive text
message_1 = most_trade_type_politician(data, selected_politician)
message_2 = most_traded_volume_politician(data, selected_politician)
message_3 = most_traded_sector_politician(data, selected_politician)
message_4 = most_sold_sector_politician(data, selected_politician)

# Display the information
st.write(f"{message_1} {message_2} {message_3} {message_4}")

# Create tabs for "Purchase" and "Sale"
tabs = st.tabs(["Purchase 📈", "Sale 📉"])
with tabs[0]:
    if message_3 == "They have not invested in EQUITY either.":
        st.write("There are no documented Purchases.")
    else:
        purchase = "Purchase"
        col1, col2 = st.columns(2)
        with col1:
            try:
                visualizer = Politician_Data_Visualizer(data)
                chart_pie_chart_exposure_1 = visualizer.pie_chart_advanced(
                    purchase, "quoteType", selected_politician
                )
                st.plotly_chart(chart_pie_chart_exposure_1, use_container_width=True, use_svg=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

        with col2:
            try:
                visualizer = Politician_Data_Visualizer(data)
                chart_pie_chart_exposure_2 = visualizer.pie_chart_advanced(
                    purchase, "sectorKey", selected_politician
                )
                st.plotly_chart(chart_pie_chart_exposure_2, use_container_width=True, use_svg=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

with tabs[1]:
    if message_4 == "They did not perform any sales of EQUITY during the documented time period.":
        st.write("There are no documented Sales for the polician.")
    else:
        purchase = "Sale"
        col1, col2 = st.columns(2)
        with col1:
            try:
                visualizer = Politician_Data_Visualizer(data)
                chart_pie_chart_exposure_1 = visualizer.pie_chart_advanced(
                    purchase, "quoteType", selected_politician
                )
                st.plotly_chart(chart_pie_chart_exposure_1, use_container_width=True, use_svg=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")

        with col2:
            try:
                visualizer = Politician_Data_Visualizer(data)
                chart_pie_chart_exposure_2 = visualizer.pie_chart_advanced(
                    purchase, "sectorKey", selected_politician
                )
                st.plotly_chart(chart_pie_chart_exposure_2, use_container_width=True, use_svg=True)
            except Exception as e:
                st.error(f"Error generating chart: {e}")


# Individual Investments
st.subheader("Main Individual Investments")
st.write(f"Here you can see {selected_politician}'s five most purchased and sold instruments per type.")
st.write("Firstly, select whether you are interested in Purchases or Sales:")

# Ensure session state for `purchase_section_three` exists
if "purchase_section_three" not in st.session_state:
    st.session_state.purchase_section_three = "Purchase"

# Create tabs for Purchases and Sales
tab_purchase, tab_sale = st.tabs(["Purchases 📈", "Sales 📉"])
with tab_purchase:
    if "Purchase" not in data[data["Politician"] == selected_politician].Transaction.unique():
        st.write("There are no documented Purchases.")
    else:
        st.session_state.purchase_section_three = "Purchase"

        list_of_types_of_instruments = list(
            map(
                str,
                data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")].quoteType.unique()
            )
        )
        list_of_types_of_instruments.sort()
        selected_type_of_instrument_section_three = st.selectbox(
            "Select an instrument:",
            options=list_of_types_of_instruments,
        )

        section_three_purchase_table(
            data, list_of_types_of_instruments, selected_politician,
            "Purchase", selected_type_of_instrument_section_three
        )

with tab_sale:
    if "Sale" not in data[data["Politician"] == selected_politician].Transaction.unique():
        st.write("There are no documented Sales.")
    else:
        st.session_state.purchase_section_three = "Sale"

        list_of_types_of_instruments = list(
            map(
                str,
                data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Sale")].quoteType.unique()
            )
        )
        list_of_types_of_instruments.sort()
        selected_type_of_instrument_section_three = st.selectbox(
            "Select an instrument:",
            options=list_of_types_of_instruments,
            key="Sale"
        )

        section_three_purchase_table(
            data, list_of_types_of_instruments, selected_politician,
            "Sale", selected_type_of_instrument_section_three
        )


# Most active days
st.subheader("Most active days")

# Get information for interactive text
most_active_purchase_value = most_active_purchase(data, selected_politician)
most_active_sell_value = most_active_sell(data, selected_politician)

# Display the information
st.write(f"{most_active_purchase_value} \n \n {most_active_sell_value}")

try:
    visualizer = Politician_Data_Visualizer(data)
    barchart_five_days = visualizer.five_days_graph(selected_politician)
    st.plotly_chart(barchart_five_days, use_container_width=True, use_svg=True)
except Exception as e:
    st.error(f"Error generating chart: {e}")
