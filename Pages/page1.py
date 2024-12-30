import streamlit as st
from Src.visualization.graphs import pie_chart_advanced
from Src.visualization.graphs import grouping_for_graph
from Src.scraping.scraper import load_senators_trading
from Src.scraping.scraper import load_financial_instruments
from Src.scraping.scraper_utils import senators_data_preparation
from Src.visualization.graphs_utils import get_the_color


# Page1.py
import streamlit as st

#Load unique politicians
data_senators = load_senators_trading()
data_instrumeents = load_financial_instruments()
data = data_senators.merge(data_instrumeents, how = "left", on = "Ticker")

list_of_politicians = data.Politician.unique()
list_of_politicians.sort()

def page1():
    st.title("Get to know a politician 👨‍💼🏛️")
    st.write("On this page, you may browse through the investing history of the US politicians. \
              You may find there their trading activity, exposure to the market and many interesting information.")
    selected_politician = st.selectbox(
                                "Select a politician:",
                                options=list_of_politicians
                                      )
    st.write(f"Displaying information about: {selected_politician}")
    try:
        chart_invested_in_time = grouping_for_graph("Politician", selected_politician, data)
        st.plotly_chart(chart_invested_in_time, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")


    st.write(f"Displaying {selected_politician}'s exposure to the market:")
    try:
        chart_pie_chart_exposure = pie_chart_advanced(data, "Purchase", "quoteType", selected_politician)
        st.plotly_chart(chart_pie_chart_exposure, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {e}")



if __name__ == "__main__":
    page1()