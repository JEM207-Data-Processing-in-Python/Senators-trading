"""
This module contains the help functions for scraper.py module
"""
import os
import pandas as pd
import numpy as np
import logging
from typing import List, Optional


def load_data(filepath: str, columns: List[str]) -> pd.DataFrame:
    """
    Helper function to load a dataset from a CSV file. If the file does not
    exist, create it with the given columns.

    Args:
        filepath (str): The path to the CSV file.
        columns (List[str]): A list of column names for the DataFrame.

    Returns:
        pd.DataFrame: The loaded DataFrame or an empty DataFrame with the
        specified columns if the file doesn't exist.
    """
    try:
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            # Create an empty file with the specified columns
            pd.DataFrame(columns=columns).to_csv(filepath, index=False)
            return pd.DataFrame(columns=columns)
    except Exception as e:
        logging.error(f"Error loading {os.path.basename(filepath)}: {e}")
        return pd.DataFrame(columns=columns)


def get_last_current_data(current_data: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieve the last row of the current data if it exists.

    Parameters:
    - current_data: A pandas DataFrame containing the current senators trading
    data.

    Returns:
    - A pandas DataFrame containing the last row if exists, else None.
    """
    try:
        if current_data.empty:
            return None
        return current_data.iloc[0].to_frame().T.reset_index(drop=True)
    except Exception as e:
        logging.error(f"Error in get_last_current_data: {e}")
        return None


def delete_exclude_tickers(exclude_tickers: pd.DataFrame,
                           current_data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with tickers in the exclusion list from the current dataset.

    Parameters:
    - exclude_tickers: A pandas DataFrame containing the excluded tickers.
    - current_data: A pandas DataFrame containing the current senators trading
    data.

    Returns:
    - A pandas DataFrame after excluding the specified tickers.
    """
    try:
        exclude_tickers_set = set(exclude_tickers['Ticker'])
        return current_data[~current_data["Ticker"].isin(exclude_tickers_set)]
    except Exception as e:
        logging.error(f"Error in delete_exclude_tickers: {e}")
        return current_data


def senators_data_preparation(data: pd.DataFrame,
                              exclude_tickers: pd.DataFrame) -> pd.DataFrame:
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
        data[["Min", "Max"]] = data["Amount"].str.split(" - ", expand=True) \
            .astype(float)

        # Change to the datetime format for "Traded" and "Filed"
        data["Traded"] = pd.to_datetime(
            data["Traded Date"], format="%b %d, %Y"
        ).dt.strftime("%Y-%m-%d")
        data["Filed"] = pd.to_datetime(
            data["Filed Date"], format="%b %d, %Y"
        ).dt.strftime("%Y-%m-%d")

        # Calculate the adjusted investment, since sale should decrease your
        # total invested amount
        data["Invested"] = np.where(data["Transaction"] == "Purchase",
                                    (data["Min"] + data["Max"]) / 2,
                                    -(data["Min"] + data["Max"]) / 2)

        # Drop the unnecessary columns
        data.drop(columns=["Amount", "Min", "Max", "Traded Date", "Filed Date"],
                  inplace=True)

        # Drop all with tickers longer than 5 characters and those in
        # exclude_tickers
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
        # Filter from 2013, keep only the "Close" and "Date" columns, round the
        # "Close" values, and change the date format
        data = data.loc[data["Date"] >= "2013-01-01", ["Close", "Date"]]
        data["Close"] = data["Close"].round(2)
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce').dt.strftime(
            "%Y-%m-%d")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    return data


def fin_info_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    The function chooses only the relevant columns from the financial
    information.
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
        data: pd.DataFrame - The tickers to be filtered (Assumed to be a list
        of tickers).
    Returns:
        pd.DataFrame - The cleaned tickers, excluding those in the
        exclude_tickers.csv file.
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
    - current_data: A pandas DataFrame containing current financial instrument
    data.
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


def add_to_exclude_tickers(ticker: str, exclude_tickers: pd.DataFrame) -> pd.DataFrame:
    """
    Add a ticker to the exclude list if it's not already present.

    Parameters:
    - ticker: A string representing the stock ticker.
    - exclude_tickers: A pandas DataFrame containing the list of excluded
    tickers.

    Returns:
    - The updated exclude_tickers DataFrame.
    """
    try:
        if ticker not in exclude_tickers["Ticker"].values:
            exclude_tickers = pd.concat(
                [exclude_tickers, pd.DataFrame({"Ticker": [ticker]})],
                ignore_index=True
            )
        return exclude_tickers
    except Exception as e:
        logging.error(f"Error adding ticker {ticker} to exclude list: {e}")
        return exclude_tickers


def get_profile_picture(images: List[str]) -> Optional[str]:
    """
    Filters out irrelevant images and returns the first valid profile picture
    from a list of image URLs.

    Args:
        images (List[str]): A list of image URLs (strings).

    Returns:
        Optional[str]: The URL of the first valid profile picture, or None if
        no valid image is found.
    """
    excluded_keywords = ["logo", "icon", "flag", "coat_of_arms", "seal"]
    filtered_images = [
        img for img in images if not any(keyword in img.lower() for keyword in
                                         excluded_keywords)
    ]
    return filtered_images[0] if filtered_images else None
