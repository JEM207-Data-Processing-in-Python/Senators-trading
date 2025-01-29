"""
This is a test file for the scraper_utils_2.py file.
"""
import pytest
import pandas as pd
from Src.scraping.scraper_utils_2 import fin_history_preparation, fin_info_preparation, fin_ticker_preparation, is_data_up_to_date


@pytest.fixture
def sample_financial_data():
    # Sample data for fin_history_preparation DataFrame
    data = {
        "Date": ["2012-12-31", "2013-01-01", "2014-06-15", "2020-11-20"],
        "Close": [123.456, 134.567, 150.567, 180.678]
    }
    return pd.DataFrame(data)


def test_fin_history_preparation(sample_financial_data):
    # Test function
    cleaned_data = fin_history_preparation(sample_financial_data)

    assert isinstance(cleaned_data, pd.DataFrame)
    assert len(cleaned_data) == 3
    assert cleaned_data["Close"].iloc[0] == 134.57
    assert cleaned_data["Date"].iloc[0] == "2013-01-01"


@pytest.fixture
def sample_fin_info_data():
    # Sample data for fin_info_preparation DataFrame
    data = {
        "Ticker": ["AAPL", "GOOG", "TSLA"],
        "quoteType": ["Equity", "Equity", "Equity"],
        "longName": ["Apple Inc.", "Alphabet Inc.", "Tesla Inc."],
        "shortName": ["AAPL", "GOOG", "TSLA"],
        "city": ["Cupertino", "Mountain View", "Palo Alto"],
        "country": ["USA", "USA", "USA"],
        "industryKey": [1, 2, 3],
        "sectorKey": [4, 5, 6],
        "longBusinessSummary": ["Tech", "Tech", "Auto"],
        "financialCurrency": ["USD", "USD", "USD"],
        "currency": ["USD", "USD", "USD"],
        "irrelevantColumn": [10, 20, 30]
    }
    return pd.DataFrame(data)


def test_fin_info_preparation(sample_fin_info_data):
    # Test function
    cleaned_data = fin_info_preparation(sample_fin_info_data)
    assert isinstance(cleaned_data, pd.DataFrame)
    assert set(cleaned_data.columns) == {
        "Ticker", "quoteType", "longName", "shortName",
        "city", "country", "industryKey", "sectorKey",
        "longBusinessSummary", "financialCurrency", "currency"
    }
    assert "irrelevantColumn" not in cleaned_data.columns


@pytest.fixture
# Sample data for fin_ticker_preparation DataFrame
def sample_ticker_data():
    return ["AAPL", "GOOG", "TSLA", "AMZN"]


@pytest.fixture
# Sample data for exclude_tickers_data DataFrame
def exclude_tickers_data():
    data = {
        "Ticker": ["GOOG", "AMZN"]
    }
    return pd.DataFrame(data)


def test_fin_ticker_preparation(sample_ticker_data, exclude_tickers_data):
    # Test function
    filtered_data = fin_ticker_preparation(sample_ticker_data, exclude_tickers_data)
    assert isinstance(filtered_data, list)
    assert "GOOG" not in filtered_data
    assert "AMZN" not in filtered_data
    assert "AAPL" in filtered_data
    assert "TSLA" in filtered_data


@pytest.fixture
def sample_current_data():
    # Sample data for current_data DataFrame
    data = {
        "Ticker": ["AAPL", "GOOG", "TSLA"],
        "2025-01-01": [134.57, 2750.00, 650.30],
        "2025-01-02": [136.00, 2800.00, 660.00]
    }
    return pd.DataFrame(data)


def test_is_data_up_to_date(sample_current_data):
    # Test function
    result = is_data_up_to_date(sample_current_data, "AAPL")
    assert isinstance(result, bool)
    assert not result
