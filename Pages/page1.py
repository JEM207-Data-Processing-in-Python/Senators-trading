import streamlit as st
from Src.visualization.graphs import pie_chart_advanced
from Src.visualization.graphs import grouping_for_graph
from Src.scraping.scraper import load_senators_trading
from Src.scraping.scraper import load_financial_instruments
from Src.scraping.scraper_utils import senators_data_preparation
from Src.visualization.graphs_utils import get_the_color
from Src.visualization.tables import top_five_purchased_stocks
from Src.visualization.graphs import grouping_for_barchart
from Src.page_1_help_functions.information_gather import party_politician
from Src.page_1_help_functions.information_gather import chmaber_politician
from Src.page_1_help_functions.information_gather import first_trade_politician
from Src.page_1_help_functions.information_gather import last_trade_politician
from Src.page_1_help_functions.information_gather import total_invested_politician
from Src.page_1_help_functions.information_gather import total_sold_politician
from Src.page_1_help_functions.information_gather import most_trade_type_politician
from Src.page_1_help_functions.information_gather import most_traded_volume_politician
from Src.page_1_help_functions.information_gather import most_traded_sector_politician
from Src.page_1_help_functions.information_gather import most_sold_sector_politician

# Page1.py
import streamlit as st

#Original data
data_senators = load_senators_trading()
data_instrumeents = load_financial_instruments()
data = data_senators.merge(data_instrumeents, how = "left", on = "Ticker")

#Lists for Interactive Buttons:
list_of_politicians = data.Politician.unique()
list_of_types_of_instruments = list(map(str, data.quoteType.unique()))

list_of_politicians.sort()
list_of_types_of_instruments.sort()

#Page definition
def page1():
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
    
    col1, col2 = st.columns(2)

    # Button to show the bar chart (Total Investment per Month)
    st.write(f"To display the history of trading activity of {selected_politician}, select one of the buttons. Barchart displays their trading activity\
             summarized by month. Linechart displays the trading activity continuosly:")
    st.markdown("""
        <style>
            .stButton > button {
                display: inline-block;
                margin-right: 10px;
            }
        </style>
        """, unsafe_allow_html=True)

    # Button 1
    button_bar_chart = st.button("📊")

    # Button 2
    button_line_chart = st.button("📈")

    if button_bar_chart:
        try:
            barchart_invested_in_time = grouping_for_barchart("Politician", selected_politician, data)
            st.plotly_chart(barchart_invested_in_time, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating chart: {e}")

    elif button_line_chart:
        try:
            chart_invested_in_time = grouping_for_graph("Politician", selected_politician, data)
            st.plotly_chart(chart_invested_in_time, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating chart: {e}")

    else:
        try:
            barchart_invested_in_time = grouping_for_barchart("Politician", selected_politician, data)
            st.plotly_chart(barchart_invested_in_time, use_container_width=True)
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
    
    #Charts
    st.write("Select, whether you want to see the graphs for Purchases or Sales:")
    button_purchase = None
    button_sale = None

    if message_3 == "They has not invested in EQUITY either.":
        button_sale = st.button("Sale 📉")
    elif message_4 == "They did not perform any sales of EQUITY during the documented time period.":
        button_purchase = st.button("Purchase 📈")
    else:
        button_purchase = st.button("Purchase 📈")
        button_sale = st.button("Sale 📉")
    
    if button_purchase:
        purchase = "Purchase"
    elif button_sale:
        purchase = "Sale"
    elif message_3 == "They has not invested in EQUITY either.":
        purchase = "Sale"
    elif message_4 == "They did not perform any sales of EQUITY during the documented time period.":
        purchase = "Purchase"
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


    #THIRD SECTION
    st.subheader("Main individual investitions")



    selected_type_of_instrument = st.selectbox(
                                    "Select an instrument:",
                                    options=list_of_types_of_instruments
                                      )

    st.subheader(f"Displaying the most traded stocks for {selected_politician}")
    try:
        top_five_table = top_five_purchased_stocks(data, selected_politician, selected_type_of_instrument)
        st.table(top_five_table)
    except Exception as e:
        st.error(f"Error generating chart: {e}")






if __name__ == "__main__":
    page1()