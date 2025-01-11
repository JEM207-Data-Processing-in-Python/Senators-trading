"""
This module contains the help functions for scraper.py module
"""

import pandas as pd
import logging


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

def is_data_up_to_date(current_data: pd.DataFrame, ticker: str) -> bool:
    """
    Check if the data for a given ticker is up-to-date.

    Parameters:
    - current_data: A pandas DataFrame containing current financial instrument data.
    - ticker: A string representing the stock ticker.

    Returns:
    - A boolean indicating whether the data is up-to-date.
    """
    try:
        today = pd.Timestamp.today()
        first_day_current_month = today.replace(day=1)
        ticker_data = current_data[current_data["Ticker"] == ticker]

        if not ticker_data.empty:
            last_date = ticker_data.columns[-1]
            return last_date == first_day_current_month.strftime('%Y-%m-%d')

        return False
    except Exception as e:
        logging.error(f"Error checking if data is up-to-date for {ticker}: {e}")
        return False