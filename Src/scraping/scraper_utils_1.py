"""
This module contains the help functions for scraper.py module
"""
import os
import pandas as pd
import numpy as np
import logging
from typing import List


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
