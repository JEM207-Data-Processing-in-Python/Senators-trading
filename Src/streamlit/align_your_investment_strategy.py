"""
This file contains the helper code for the Streamlit app's Align Your
Investment Strategy page.
"""
import streamlit as st
import pandas as pd
from typing import List, Tuple

from Src.scraping.scraper import DataLoader
from Src.visualization.graphs_align_investment import Pie_Chart_Align_Investment
from Src.visualization.tables import data_for_strategy_align_type, \
    data_for_strategy_align_sector


def load_and_merge_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    This function loads senators' trading data and financial instruments data,
    and merges them based on the Ticker column. Returns the filtered dataframes
    for sector and instruments with 'Unknown' values removed.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - DataFrame with sector information excluding 'Unknown'
            (`data_sector`).
            - DataFrame with instruments excluding 'Unknown'
            (`data_instruments`).
    """
    data_senators = DataLoader().load_senators_trading()
    data_instruments = DataLoader().load_financial_instruments()
    columns_to_keep = [
        "Ticker",
        "city",
        "country",
        "industryKey",
        "sectorKey",
        "longBusinessSummary",
        "currency",
        "quoteType",
        "shortName",
        "longName",
        "financialCurrency"
    ]

    data_instruments = data_instruments[columns_to_keep]
    data = data_senators.merge(data_instruments, how="left", on="Ticker")
    data = data.fillna("Unknown")
    data_sector = data[data["sectorKey"] != "Unknown"]
    data_instruments = data[data["quoteType"] != "Unknown"]

    return data_sector, data_instruments


def get_unique_sectors_and_instruments(data_instruments: pd.DataFrame,
                                       data_sector: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    This function extracts unique sectors and instruments from the provided
    data. It returns two lists: one for unique sectors and another for unique
    instruments.

    Args:
        data_instruments (pd.DataFrame): DataFrame containing instrument data.
        data_sector (pd.DataFrame): DataFrame containing sector data.

    Returns:
        Tuple[List[str], List[str]]:
            - List of unique sectors in the data (`list_of_unique_sectors`).
            - List of unique instruments in the data (`list_of_unique_instruments`).
    """
    strategy_type = data_for_strategy_align_type(data_instruments)
    strategy_sector = data_for_strategy_align_sector(data_sector)

    list_of_unique_sectors = (
        strategy_sector[strategy_sector["sectorKey"] != "Unknown"]["sectorKey"]
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

    return list_of_unique_sectors, list_of_unique_instruments


def chunk_list(lst: List[str], n: int):
    """
    Chunk a list into smaller lists of size n.

    Args:
        lst (List[str]): The list to be chunked.
        n (int): The chunk size.

    Returns:
        List[List[str]]: A list of smaller lists.
    """
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def equity_alignment_politician_sector(list_of_politicians, list_of_unique_sectors,
                                       data_general, data_user):
    """
    Compare the investment strategies of a user and multiple politicians based
    on sector allocation. It evaluates the alignment of investments between the
    user and each politician and visualizes the results with pie charts
    representing sector-based investment distributions.

    Parameters:
    - list_of_politicians (List[str]): A list of politician names to compare
    against the user's strategy.
    - list_of_unique_sectors (List[str]): A list of unique sector names for
    consistent color mapping in pie charts.
    - data_general (pd.DataFrame): The general investment data of politicians,
    sector-wise.
    - data_user (pd.DataFrame): The user's investment data by sector.

    Returns:
    - None: Displays pie charts and textual information using Streamlit.
    """
    pie_chart_creator = Pie_Chart_Align_Investment(list_of_unique_sectors)
    strategy_data = data_for_strategy_align_sector(data_general)
    help_df = strategy_data.merge(data_user, how="left", on="sectorKey")
    help_df["alignment"] = (
        (1 - abs(help_df["Total Invested Sector"] - help_df["Invested by User"]) /
         help_df["Total Invested Sector"].replace(0, 1)).clip(lower=0)
    )
    tabs = st.tabs(list_of_politicians)
    for i, tab in enumerate(tabs):
        with tab:
            st.header(f"Comparison with {list_of_politicians[i]}")

            info_table = help_df[help_df["Politician"] == list_of_politicians[i]]\
                .sort_values(by="alignment", ascending=False)

            # Display textual information about the most and least aligned sectors
            if not info_table.empty:
                st.write(
                    f"Your strategy is the most compatible with the strategy of "
                    f"{list_of_politicians[i]}. The biggest compliance is in the "
                    f"{info_table['sectorKey'].iloc[0]} sector "
                    f"({info_table['alignment'].iloc[0] * 100:.2f}%). The lowest "
                    f"compliance is in the {info_table['sectorKey'].iloc[-1]} sector "
                    f"({info_table['alignment'].iloc[-1] * 100:.2f}%)."
                )
            else:
                st.write(f"No data available for {list_of_politicians[i]}.")

            col_politician, col_user = st.columns(2)
            with col_politician:
                chart_pie = pie_chart_creator.create_politician_chart(
                    data=data_general,
                    purchase="Purchase",
                    subset="sectorKey",
                    politician=list_of_politicians[i]
                )
                st.plotly_chart(chart_pie, use_container_width=True,
                                key=f"Politician_{list_of_politicians[i]}_graph",
                                use_svg=True)

            with col_user:
                chart_pie_2 = pie_chart_creator.create_user_chart(
                    data=data_user,
                    what="sectorKey"
                )
                st.plotly_chart(chart_pie_2, use_container_width=True,
                                key=f"User_graph_{list_of_politicians[i]}",
                                use_svg=True)


def equity_alignment_politician_instrument(list_of_politicians, list_of_unique_instruments,
                                           data_general, data_user):
    """
    Compare the investment strategies of a user and multiple politicians based
    on the type of financial instrument. It evaluates the alignment of
    investments between the user and each politician and visualizes the results
    with pie charts representing instrument-based investment distributions.

    Parameters:
    - list_of_politicians (List[str]): A list of politician names to compare
    against the user's strategy.
    - list_of_unique_instruments (List[str]): A list of unique financial
    instrument names for consistent color mapping in pie charts.
    - data_general (pd.DataFrame): The general investment data of politicians,
    categorized by financial instruments.
    - data_user (pd.DataFrame): The user's investment data categorized by
    financial instruments.

    Returns:
    - None: Displays pie charts and textual information using Streamlit.
    """
    pie_chart_creator = Pie_Chart_Align_Investment(list_of_unique_instruments)

    # Create tabs for each politician to compare their strategy with the user's
    tabs = st.tabs(list_of_politicians)
    for i, tab in enumerate(tabs):
        with tab:
            # Add a subheader with the politician's name
            st.subheader(f"Comparison with {list_of_politicians[i]}")
            col_politician, col_user = st.columns(2)
            with col_politician:
                chart_pie = pie_chart_creator.create_politician_chart(
                    data=data_general,
                    purchase="Purchase",
                    subset="quoteType",
                    politician=list_of_politicians[i]
                )
                st.plotly_chart(chart_pie, use_container_width=True,
                                key=f"Politician_{list_of_politicians[i]}_graph",
                                use_svg=True)

            # Create and display the user's pie chart
            with col_user:
                chart_pie_2 = pie_chart_creator.create_user_chart(
                    data=data_user,
                    what="quoteType"
                )
                st.plotly_chart(chart_pie_2, use_container_width=True,
                                key=f"User_graph_{list_of_politicians[i]}",
                                use_svg=True)
