"""
This module contains the help functions for scraper.py module
"""
import pandas as pd
import numpy as np
import logging


def senators_data_preparation(data: pd.DataFrame, exclude_tickers: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the scrapped senators data and extract all relevant information.
    Args:
        data: pd.DataFrame - The senators data to be cleaned and transformed.
        exclude_tickers: pd.DataFrame - The tickers to be excluded.
    Returns:
        pd.DataFrame - The cleaned data.
    """
    try:
        # Extract the "Type" and "Amount" from the "Transaction" column
        data["Amount"] = data["Amount"].str.replace("[$,]", "", regex=True)
        data[["Min", "Max"]] = data["Amount"].str.split(" - ", expand=True).astype(float)

        # Change to the datetime format for "Traded" and "Filed"
        data["Traded"] = pd.to_datetime(data["Traded Date"], format="%b %d, %Y").dt.strftime("%Y-%m-%d")
        data["Filed"] = pd.to_datetime(data["Filed Date"], format="%b %d, %Y").dt.strftime("%Y-%m-%d")

        # Calculate the adjusted investment, since sale should decrease your total invested amount
        data["Invested"] = np.where(data["Transaction"] == "Purchase", (data["Min"] + data["Max"]) / 2, -(data["Min"] + data["Max"]) / 2)

        # Drop the unnecessary columns
        data.drop(columns=["Amount", "Min", "Max", "Traded Date", "Filed Date"], inplace=True)

        # Drop all with tickers longer than 5 characters and those in exclude_tickers
        exclude_tickers_set = set(exclude_tickers['Ticker'])
        data = data[(data["Ticker"].str.len() <= 5) & (~data["Ticker"].isin(exclude_tickers_set))]
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    return data


def fin_history_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the history financial market data
    Args:
        data: pd.DataFrame - The history data to be cleaned.
    Returns:
        pd.DataFrame - The cleaned history data.
    """
    try:
        # Filter from 2013, keep only the "Close" and "Date" columns, round the "Close" values, and change the date format
        data = data.loc[data["Date"] >= "2013-01-01", ["Close", "Date"]]
        data["Close"] = data["Close"].round(2)
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce').dt.strftime("%Y-%m-%d")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    return data


def fin_info_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    The function chooses only the relevant columns from the financial information.
    Args:
        data: pd.DataFrame - The financial information to be cleaned.
    Returns:
        pd.DataFrame - The cleaned financial data.
    """
    # Define the set of relevant columns
    relevant_columns = {"Ticker", "quoteType", "longName", "shortName",
                        "city", "country", "industryKey", "sectorKey",
                        "longBusinessSummary", "financialCurrency", "currency"}

    try:
        # Select only the relevant columns that are present in the data
        data = data.loc[:, data.columns.intersection(relevant_columns)]
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    return data


def fin_ticker_preparation(data: pd.DataFrame, exclude_tickers: pd.DataFrame) -> pd.DataFrame:
    """
    Remove the tickers that are not found via Yahoo.
    Args:
        data: pd.DataFrame - The tickers to be filtered (Assumed to be a list of tickers).
    Returns:
        pd.DataFrame - The cleaned tickers, excluding those in the exclude_tickers.csv file.
    """
    try:
        # Exclude the tickers that are in the exclude_tickers
        exclude_tickers_set = exclude_tickers['Ticker'].to_list()
        data = [ticker for ticker in data if ticker not in exclude_tickers_set]
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    return data
