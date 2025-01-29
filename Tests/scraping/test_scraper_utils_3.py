"""
This is a test file for the scraper_utils_3.py file.
"""
import pandas as pd
from Src.scraping.scraper_utils_3 import add_to_exclude_tickers, get_profile_picture


def test_add_to_exclude_tickers():
    df = pd.DataFrame({"Ticker": ["AAPL", "GOOG", "MSFT"]})

    # Test function
    result = add_to_exclude_tickers("TSLA", df)
    assert "TSLA" in result["Ticker"].values, "Ticker should be added to the list"

    # Test function
    result = add_to_exclude_tickers("AAPL", df)
    assert len(result) == 3, "No new tickers should be added"

    empty_df = pd.DataFrame(columns=["Ticker"])
    # Test function
    result = add_to_exclude_tickers("AMZN", empty_df)
    assert "AMZN" in result["Ticker"].values, "Ticker should be added to empty list"


def test_get_profile_picture():
    images = [
        "http://example.com/profile1.jpg",
        "http://example.com/logo.png",
        "http://example.com/flag.jpg"
    ]

    # Test function
    result = get_profile_picture(images)
    assert result == "http://example.com/profile1.jpg", "Should return the first valid image"

    images = [
        "http://example.com/logo.png",
        "http://example.com/flag.jpg"
    ]

    # Test function
    result = get_profile_picture(images)
    assert result is None, "Should return None when no valid image is found"

    images = [
        "http://example.com/profile1.jpg",
        "http://example.com/profile2.jpg"
    ]

    # Test function
    result = get_profile_picture(images)
    assert result == "http://example.com/profile1.jpg", "Should return the first valid image"
