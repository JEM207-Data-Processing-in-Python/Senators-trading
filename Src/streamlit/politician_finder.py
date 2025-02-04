"""
This file contains the helper code for the Streamlit app's Politician Finder.
"""
import pandas as pd
import streamlit as st

from Src.visualization.tables import top_five_purchased_stocks
from Src.visualization.tables import top_five_sold_stocks
from Src.scraping.scraper import DataLoader


def party_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Retrieves the political party of the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician information.
    - selected_politician (str): The name of the politician to look for in the
    dataset.

    Returns:
    - str: The name of the political party the selected politician belongs to.
           Can be 'Republican Party', 'Democratic Party', or 'Third Party'.

    Note:
    - Error handling should be added for invalid or missing politician names.
    """
    # Get information for interactive text
    party_politician = data[data["Politician"] == selected_politician][
        "Party"].unique()

    # Determine the party based on the value in the 'Party' column
    if party_politician == "R":
        party_politician = "Republican Party"
    elif party_politician == "D":
        party_politician = "Democratic Party"
    else:
        party_politician = "Third Party"

    return party_politician


def first_trade_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Retrieves the date of the first trade for the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician trading data.
    - selected_politician (str): The name of the politician whose first trade
    is to be retrieved.

    Returns:
    - str: The date of the first trade for the selected politician.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Get the date of the first trade by filtering the data for the selected
    # politician
    first_trade_politician = data[data["Politician"] == selected_politician][
        "Traded"].min()

    return first_trade_politician


def last_trade_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Retrieves the date of the last trade for the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician trading data.
    - selected_politician (str): The name of the politician whose last trade is
    to be retrieved.

    Returns:
    - str: The date of the last trade for the selected politician.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Get the date of the last trade by filtering the data for the selected
    # politician
    last_trade_politician = data[data["Politician"] == selected_politician][
        "Traded"].max()

    return last_trade_politician


def total_invested_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Calculates the total amount invested by the selected politician in
    purchases.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician transaction data.
    - selected_politician (str): The name of the politician whose total
    investments are to be calculated.

    Returns:
    - str: The total amount invested in purchases formatted with commas for
    thousands.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Calculate total invested by the selected politician on purchase
    # transactions
    total_invested_politician = data[
        (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
    ]["Invested"].sum()

    # Format the result for readability
    total_invested_politician = f"{total_invested_politician:,.0f}"

    return total_invested_politician


def total_sold_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Calculates the total amount sold by the selected politician in sales.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician transaction data.
    - selected_politician (str): The name of the politician whose total sales
    are to be calculated.

    Returns:
    - str: The total amount sold in sales formatted with commas for thousands.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    help_df = data.copy()

    # Reverse the 'Invested' value for sale transactions to ensure a negative
    # total
    help_df["Invested"] = -help_df["Invested"]

    # Calculate total sold by the selected politician on sale transactions
    total_sold_politician = help_df[
        (help_df["Politician"] == selected_politician) & (help_df["Transaction"] == "Sale")
    ]["Invested"].sum()

    # Format the result for readability
    total_sold_politician = f"{total_sold_politician:,.0f}"

    return total_sold_politician


def most_trade_type_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most frequent trade type (quoteType) the selected politician
    invests in, based on the "Purchase" transactions in the dataset.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating which trade type the politician invests the
    most in.

    Note:
    - Returns a message about purchases if they exist; otherwise, indicates no
    purchases.
    """
    try:
        most_trade_type_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
        ]
            .groupby("quoteType", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["quoteType"]
        )

        message_1 = (
            f"{selected_politician} invests the most often into "
            f"{most_trade_type_politician}"
        )
    except Exception:
        message_1 = (f"{selected_politician} has not performed any purchases "
                     "during documented time period.")

    return message_1


def most_traded_volume_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the total volume of the most traded instrument (quoteType) by
    the selected politician, based on "Purchase" transactions.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the total average amount purchased by the
    politician.

    Note:
    - Returns the amount purchased for the most traded instrument or an empty
    string if no data is available.
    """
    try:
        most_traded_volume_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
        ]
            .groupby("quoteType", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["Invested"]
        )
        most_traded_volume_politician = f"{most_traded_volume_politician:,.0f}"

        message_2 = (
            f"with the total average amount purchased of "
            f"{most_traded_volume_politician} USD."
        )
    except Exception:
        message_2 = ""

    return message_2


def most_traded_sector_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most traded sector and its total volume for equity
    investments (quoteType == 'EQUITY') by the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the most traded sector for equity investments
    and its total volume.

    Note:
    - Returns a message about equity investments in a sector if available;
    otherwise, indicates no data.
    """
    try:
        most_traded_sector_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["sectorKey"]
        )
    except Exception:
        most_traded_sector_politician = "Empty"

    try:
        most_traded_sector_volume = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["Invested"]
        )
        most_traded_sector_volume = f"{most_traded_sector_volume:,.0f}"

    except Exception:
        most_traded_sector_volume = "Empty"

    if most_traded_sector_politician == "Empty":
        message_3 = "They have not invested in EQUITY either."
    else:
        message_3 = (
            f"When it comes to EQUITY, this politician mostly invests in "
            f"{most_traded_sector_politician} with the total average volume "
            f"invested of {most_traded_sector_volume} USD."
        )

    return message_3


def most_sold_sector_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most sold sector and its total volume for equity sales
    (quoteType == 'EQUITY') by the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the most sold sector for equity sales and its
    total volume.

    Note:
    - Returns a message about equity sales in a sector if available; otherwise,
    indicates no data.
    """
    try:
        most_sold_sector_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Sale") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[-1]["sectorKey"]
        )
    except Exception:
        most_sold_sector_politician = "Empty"

    try:
        most_sold_sector_volume = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Sale") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[-1]["Invested"]
        )

        most_sold_sector_volume = f"{-most_sold_sector_volume:,.0f}"
    except Exception:
        most_sold_sector_volume = "Empty"

    if most_sold_sector_politician == "Empty":
        message_4 = (
            "They did not perform any sales of EQUITY during the documented "
            "time period."
        )
    else:
        message_4 = (
            f"{selected_politician} sold EQUITY mostly in "
            f"{most_sold_sector_politician} sector with the total average "
            f"volume sold of {most_sold_sector_volume} USD."
        )

    return message_4


def wikipedia_information(selected_politician: str) -> tuple:
    """
    This function retrieves the additional information about a selected
    politician, including their Wikipedia link and a picture (if available)
    from a dataset.

    Args:
    - selected_politician (str): The name of the politician whose information
    is to be fetched.

    Returns:
    - tuple: A tuple containing:
      1. A string with additional information about the politician (or a
      default message if not available).
      2. A string with the URL of the politician's Wikipedia page (or a default
      message if not available).
      3. A string with the file path or URL of the politician's picture (or a
      default message if not available).
    """
    data = DataLoader().load_senators_information()
    data = data[data["Politician"] == selected_politician]

    if data.empty:
        return None, None, None

    information = data["Information"].values[0]
    link = data["Link"].values[0]
    picture = data["Picture"].values[0]

    return information, link, picture


def chamber_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    This function retrieves the chamber of a selected politician from a dataset
    and returns its full descriptive name. If the politician's chamber is not
    found, it returns 'Unknown Chamber'.

    Args:
    - data (pandas.DataFrame): A DataFrame containing at least two columns:
      'Politician' for the politician's name and 'Chamber' for the chamber they
      belong to.
    - selected_politician (str): The name of the politician whose chamber is to
    be identified.

    Returns:
    - str: The full name of the chamber the selected politician belongs to.
      The returned string is one of the following:
        - 'House of Representatives' if the politician belongs to the House.
        - 'Senate' if the politician belongs to the Senate.
        - 'Unknown Chamber' if the chamber is not identified or found.
    """
    chamber_politician = data[data["Politician"] == selected_politician][
        "Chamber"].unique()
    if chamber_politician == "House":
        chamber_politician = "House of Representatives"
    elif chamber_politician == "Senate":
        chamber_politician = "Senate"
    else:
        chamber_politician = "Unknown Chamber"

    return chamber_politician


def individual_invest_politician(data: pd.DataFrame, list: list,
                                 selected_politician: str) -> str:
    """
    This function generates a summary message for a selected politician's top
    investments in different quote types. It fetches the most popular
    investment for each quote type and returns a concatenated message with the
    investment details.

    Args:
    - data (pandas.DataFrame): A DataFrame containing investment information,
    including columns such as 'Name', 'Total Invested', and other relevant data.
    - list (list): A list of quote types (str) for which the investments are to
    be summarized.
    - selected_politician (str): The name of the politician whose investment
    information is to be retrieved.

    Returns:
    - str: A string containing a concatenated message that summarizes the top
    investments for each quote type and the total amount invested.
    """
    message = []
    for quoteType in list:
        help_df = top_five_purchased_stocks(data, selected_politician, quoteType)
        sub_message = (
            f"in {quoteType}, where the most popular investment is "
            f"{help_df.iloc[0]['Name']} with a total amount invested of "
            f"{help_df.iloc[0]['Total Invested']}"
        )
        message.append(sub_message)

    final_message = "; ".join(message)

    return final_message


def individual_sell_politician(data: pd.DataFrame, list: list,
                               selected_politician: str) -> str:
    """
    Generates a summary of the most sold stocks for a selected politician
    across multiple quote types.

    Args:
    - data (pandas.DataFrame): DataFrame with sales information, including
    'Politician', 'Name', and 'Total Sold'.
    - list (list): List of quote types to summarize.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A concatenated message summarizing the most sold stock for each
    quote type and the total amount sold.

    Raises:
    - ValueError: If the politician is not found or no data for a quote type.
    - KeyError: If required columns are missing.
    """
    message = []

    if selected_politician not in data['Politician'].values:
        raise ValueError(
            f"Politician '{selected_politician}' not found in the data."
        )

    for quoteType in list:
        try:
            help_df = top_five_sold_stocks(data, selected_politician, quoteType)
            if help_df.empty:
                raise ValueError(
                    f"No data found for {selected_politician} in {quoteType}."
                )

            sub_message = (
                f"in {quoteType}, where the most sold was "
                f"{help_df.iloc[0]['Name']} with a total amount sold of "
                f"{help_df.iloc[0]['Total Sold']}"
            )
            message.append(sub_message)

        except KeyError as e:
            raise KeyError(f"Missing expected column: {str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while processing {quoteType}: {str(e)}")

    final_message = "; ".join(message)

    return final_message


def section_three_purchase_table(
    data: pd.DataFrame,
    list_of_types_of_instruments: list,
    selected_politician: str,
    purchase: str,
    selected_type_of_instrument_section_three: str
) -> None:
    """
    Displays a table of the most purchased or sold stocks for a selected
    politician, along with their investments or sales in specific instrument
    types.

    Args:
    - data (pandas.DataFrame): A DataFrame containing information about stocks,
    purchases, and sales.
    - list_of_types_of_instruments (list): A list of instrument types that the
    politician has invested in or sold.
    - selected_politician (str): The name of the politician whose purchases or
    sales are to be displayed.
    - purchase (str): A string that determines whether to display "Purchase" or
    "Sale" data.
    - selected_type_of_instrument_section_three (str): The type of instrument
    to display in the table (e.g., stock type).

    Returns:
    - None: This function does not return anything but displays information
    using `st.write()` and `st.table()`.

    Exceptions:
    - If an error occurs while fetching or displaying the table data, an error
    message will be shown.
    """
    if purchase == "Purchase":
        if list_of_types_of_instruments and len(list_of_types_of_instruments) > 0:
            list_of_top_individual_invest = (
                f"{selected_politician} has invested in "
                f"{', '.join(list_of_types_of_instruments)}. They invest "
                f"{individual_invest_politician(data, list_of_types_of_instruments, selected_politician)}."
            )
            st.write(list_of_top_individual_invest)

            st.caption(
                f"Displaying the most traded "
                f"{selected_type_of_instrument_section_three} for "
                f"{selected_politician}"
            )
            try:
                top_five_table = top_five_purchased_stocks(
                    data, selected_politician, selected_type_of_instrument_section_three
                )
                st.table(top_five_table)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.write(
                f"{selected_politician} did not purchase any instruments "
                "in the documented time period."
            )

    elif purchase == "Sale":
        if list_of_types_of_instruments and len(list_of_types_of_instruments) > 0:
            list_of_top_individual_sold = (
                f"{selected_politician} has sold "
                f"{', '.join(list_of_types_of_instruments)}. They sold "
                f"{individual_sell_politician(data, list_of_types_of_instruments, selected_politician)}."
            )
            st.write(list_of_top_individual_sold)

            st.caption(
                f"Displaying the most sold "
                f"{selected_type_of_instrument_section_three} for "
                f"{selected_politician}"
            )
            try:
                top_five_table_sold = top_five_sold_stocks(
                    data, selected_politician, selected_type_of_instrument_section_three
                )
                st.table(top_five_table_sold)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.write(
                f"{selected_politician} did not sell any instruments in "
                "the documented time period."
            )


def five_days(data: pd.DataFrame, selected_politician: str) -> pd.DataFrame:
    """
    This function retrieves the top 5 most invested and the 5 least invested
    stock trades by a selected politician, based on their purchase and sale
    transactions.

    Args:
    - data (pandas.DataFrame): A DataFrame containing transaction data with
    columns such as 'Politician', 'Transaction', 'Traded', and 'Invested'.
    - selected_politician (str): The name of the politician whose transactions
    are to be analyzed.

    Returns:
    - pandas.DataFrame: A DataFrame containing the top 5 most invested and the
    5 least invested stock trades, sorted by investment amount.
    """
    help_df_purchase = data[
        (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
    ].copy()
    help_df_sale = data[
        (data["Politician"] == selected_politician) & (data["Transaction"] == "Sale")
    ].copy()

    top_five = (
        help_df_purchase.groupby("Traded", as_index=False)["Invested"]
        .sum()
        .sort_values(by="Invested", ascending=False)
        .head(5)
    )

    last_five = (
        help_df_sale.groupby("Traded", as_index=False)["Invested"]
        .sum()
        .sort_values(by="Invested", ascending=True)
        .head(5)
    )

    final = pd.concat([top_five, last_five]).sort_values(by="Invested")

    return final


def most_active_purchase(data: pd.DataFrame, selected_politician: str) -> str:
    """
    This function generates a message about the most active purchase made by a
    selected politician during a specific period. It identifies the day with
    the highest investment, the total volume purchased, and the most purchased
    stock type.

    Args:
    - data (pandas.DataFrame): A DataFrame containing transaction data,
    including columns like 'Politician', 'Transaction', 'Traded', 'Invested',
    and 'quoteType'.
    - selected_politician (str): The name of the politician whose purchases are
    to be analyzed.

    Returns:
    - str: A message summarizing the politician's most active purchase and the
    most purchased stock type.

    Exceptions:
    - If any error occurs while processing the data, an error message is shown
    using `st.error`.
    """
    # Prepare and sort data
    help_df = five_days(data, selected_politician)
    help_df = help_df.sort_values(by="Invested", ascending=False)

    # Initialize message
    message = (f"**{selected_politician}** has not purchased any instruments "
               "during the documented period.")

    # First part of the message
    if not help_df.empty and help_df.iloc[0]["Invested"] > 0:
        most_active_purchase = help_df.iloc[0]["Traded"]
        most_active_purchase_volume = help_df.iloc[0]["Invested"]
        most_active_purchase_volume = f"{most_active_purchase_volume:,.0f}"
        message_p1 = (
            f"**{selected_politician}** invested the most on day "
            f"**{most_active_purchase}** with a total volume purchased of "
            f"**{most_active_purchase_volume}** USD."
        )

        try:
            # Filter data for the most active purchase
            help_df1 = data[
                (data["Politician"] == selected_politician) & (data["Traded"] == most_active_purchase) & (data["Transaction"] == "Purchase")].copy()

            top_five_purchases = help_df1.groupby(
                "quoteType", as_index=False
            )["Invested"].sum()
            top_five_purchases = top_five_purchases.sort_values(
                by="Invested", ascending=False
            )
            message_p2 = (
                f"The most purchased stock type is "
                f"{top_five_purchases.iloc[0]['quoteType']}."
            )
            message = f"{message_p1} {message_p2}"

        except Exception as e:
            st.error(f"Error generating purchases: {e}")

    return message


def most_active_sell(data: pd.DataFrame, selected_politician: str) -> str:
    """
    This function generates a message about the most active sale made by a
    selected politician during a specific period. It identifies the day with
    the largest sale volume, the total volume sold, and breaks down the sale by
    instrument type and sector (for EQUITY).

    Args:
    - data (pandas.DataFrame): A DataFrame containing transaction data,
    including columns like 'Politician', 'Transaction', 'Traded', 'Invested',
    'quoteType', and 'sector'.
    - selected_politician (str): The name of the politician whose sale data is
    to be analyzed.

    Returns:
    - str: A message summarizing the politician's most active sale, including
    the most sold instrument type and, if applicable, sector breakdown.

    Exceptions:
    - If any error occurs during processing, a message with relevant details is
    returned, or an error message is displayed.
    """
    help_df = five_days(data, selected_politician)
    help_df = help_df.sort_values(by="Invested", ascending=False)

    # Initialize message
    message = (f"{selected_politician} has not sold any instruments during the "
               "documented period.")

    # First part of the message
    if not help_df.empty and help_df.iloc[-1]["Invested"] < 0:
        most_active_sell = help_df.iloc[-1]["Traded"]
        most_active_sell_volume = -help_df.iloc[-1]["Invested"]
        most_active_sell_volume = f"{most_active_sell_volume:,.0f}"
        message_p1 = (
            f"{selected_politician} sold the most on {most_active_sell} "
            f"with a total volume sold of {most_active_sell_volume} USD."
        )

        try:
            # Filter data for the most active sale
            help_df1 = data[
                (data["Politician"] == selected_politician) & (data["Traded"] == most_active_sell) & (data["Transaction"] == "Sale")
            ].copy()

            help_df1["Invested"] = -help_df1["Invested"]
            grouped_df1 = help_df1.groupby("quoteType", as_index=False)["Invested"].sum()

            message_list = [
                f"{quoteType} in a total volume sold of "
                f"{grouped_df1[grouped_df1['quoteType'] == quoteType].iloc[0]['Invested']:,.0f} USD"
                for quoteType in grouped_df1["quoteType"].unique()
            ]

            message_p2 = (
                f" The instruments sold on this day were "
                f"{'; '.join(message_list)}."
            )

            # Additional sector-specific message for EQUITY
            if "EQUITY" in grouped_df1["quoteType"].unique():
                help_df2 = data[
                    (data["Politician"] == selected_politician) & (data["Traded"] == most_active_sell) & (data["Transaction"] == "Sale") & (data["quoteType"] == "EQUITY")
                ].copy()

                help_df2["Invested"] = -help_df2["Invested"]
                grouped_df2 = help_df2.groupby("sector", as_index=False)["Invested"].sum()

                top_3_grouped_df2 = grouped_df2.sort_values(by="Invested", ascending=False).head(3)
                message_list_1 = [
                    f"{sector} in a total volume sold of "
                    f"{top_3_grouped_df2[top_3_grouped_df2['sector'] == sector].iloc[0]['Invested']:,.0f} USD"
                    for sector in top_3_grouped_df2["sector"]
                ]

                message_p3 = (
                    f" On this day, the EQUITY sold was mainly in the "
                    f"sector: {'; '.join(message_list_1)}."
                )
                message = message_p1 + message_p2 + message_p3
            else:
                message = message_p1 + message_p2

        except (KeyError, IndexError):
            message = message_p1

    return message
