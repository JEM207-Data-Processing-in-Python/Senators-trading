"""
This module contains the help functions for scraper.py module
"""
import pandas as pd
import logging
from typing import List, Optional

def add_to_exclude_tickers(ticker: str, exclude_tickers: pd.DataFrame) -> pd.DataFrame:
    """
    Add a ticker to the exclude list if it's not already present.

    Parameters:
    - ticker: A string representing the stock ticker.
    - exclude_tickers: A pandas DataFrame containing the list of excluded tickers.

    Returns:
    - The updated exclude_tickers DataFrame.
    """
    try:
        if ticker not in exclude_tickers["Ticker"].values:
            exclude_tickers = pd.concat([exclude_tickers, pd.DataFrame({"Ticker": [ticker]})], ignore_index=True)
        return exclude_tickers
    except Exception as e:
        logging.error(f"Error adding ticker {ticker} to exclude list: {e}")
        return exclude_tickers


def get_profile_picture(images: List[str]) -> Optional[str]:
    """
    Filters out irrelevant images and returns the first valid profile picture from a list of image URLs.
    
    Args:
        images (List[str]): A list of image URLs (strings).

    Returns:
        Optional[str]: The URL of the first valid profile picture, or None if no valid image is found.
    """
    excluded_keywords = ["logo", "icon", "flag", "coat_of_arms", "seal"]
    filtered_images = [
        img for img in images if not any(keyword in img.lower() for keyword in excluded_keywords)
    ]
    return filtered_images[0] if filtered_images else None
