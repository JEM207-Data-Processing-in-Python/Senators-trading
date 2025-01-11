"""
This file contains the helper code for the Streamlit app's Politician Finder.
"""
import pandas as pd


def party_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Retrieves the political party of the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician information.
    - selected_politician (str): The name of the politician to look for in the dataset.

    Returns:
    - str: The name of the political party the selected politician belongs to.
           Can be 'Republican Party', 'Democratic Party', or 'Third Party'.

    Note:
    - Error handling should be added for invalid or missing politician names.
    """
    # Get information for interactive text
    party_politician = data[data["Politician"] == selected_politician]["Party"].unique()

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
    - selected_politician (str): The name of the politician whose first trade is to be retrieved.

    Returns:
    - str: The date of the first trade for the selected politician.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Get the date of the first trade by filtering the data for the selected politician
    first_trade_politician = data[data["Politician"] == selected_politician]["Traded"].min()

    return first_trade_politician


def last_trade_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Retrieves the date of the last trade for the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician trading data.
    - selected_politician (str): The name of the politician whose last trade is to be retrieved.

    Returns:
    - str: The date of the last trade for the selected politician.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Get the date of the last trade by filtering the data for the selected politician
    last_trade_politician = data[data["Politician"] == selected_politician]["Traded"].max()

    return last_trade_politician


def total_invested_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Calculates the total amount invested by the selected politician in purchases.

    Parameters:
    - data (pd.DataFrame): The dataset containing politician transaction data.
    - selected_politician (str): The name of the politician whose total investments are to be calculated.

    Returns:
    - str: The total amount invested in purchases formatted with commas for thousands.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    # Calculate total invested by the selected politician on purchase transactions
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
    - selected_politician (str): The name of the politician whose total sales are to be calculated.

    Returns:
    - str: The total amount sold in sales formatted with commas for thousands.

    Note:
    - Error handling should be added for missing or incorrect politician names.
    """
    help_df = data.copy()

    # Reverse the 'Invested' value for sale transactions to ensure a negative total
    help_df["Invested"] = -help_df["Invested"]

    # Calculate total sold by the selected politician on sale transactions
    total_sold_politician = help_df[
        (help_df["Politician"] == selected_politician) & (help_df["Transaction"] == "Sale")
    ]["Invested"].sum()

    # Format the result for readability
    total_sold_politician = f"{total_sold_politician:,.0f}"

    return total_sold_politician
