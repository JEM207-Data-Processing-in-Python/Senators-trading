"""
This module contains the tests for the scraper_utils module.
"""
import pandas as pd
from pandas.testing import assert_frame_equal

from Src.scraping.scraper_utils import senators_data_preparation, fin_history_preparation, fin_info_preparation, fin_ticker_preparation


def test_senators_data_preparation():
    """
    Test the senators_data_preparation function with data containing irrelevant columns.
    """
    input_data = pd.DataFrame({
        "Transaction": ["Purchase", "Sale", "Purchase"],
        "Amount": ["$1,000 - $2,000", "$500 - $1,500", "$3,000 - $4,000"],
        "Ticker": ["AAPL", "GOOG", "AMZN"],
        "Traded Date": ["Jan 01, 2020", "Feb 15, 2021", "Mar 10, 2022"],
        "Filed Date": ["Jan 02, 2020", "Feb 16, 2021", "Mar 11, 2022"]
    })
    exclude_tickers = pd.DataFrame({
        "Ticker": ["GOOG"]
    })
    expected_output = pd.DataFrame({
        "Transaction": ["Purchase", "Purchase"],
        "Ticker": ["AAPL", "AMZN"],
        "Traded": ["2020-01-01", "2022-03-10"],
        "Filed": ["2020-01-02", "2022-03-11"],
        "Invested": [1500.0, 3500.0]
    })

    result = senators_data_preparation(input_data, exclude_tickers)

    assert_frame_equal(result, expected_output)


def test_fin_history_preparation():
    """
    Test the fin_history_preparation function with data containing irrelevant columns.
    """
    input_data = pd.DataFrame({
        "Date": ["2012-12-31", "2013-01-01", "2014-05-01"],
        "Close": [100.1234, 200.5678, 300.9876],
        "Open": [99.0, 199.0, 299.0],
        "Volume": [1000, 2000, 3000]
    })
    expected_output = pd.DataFrame({
        "Date": ["2013-01-01", "2014-05-01"],
        "Close": [200.57, 300.99]
    })

    result = fin_history_preparation(input_data).round({'Close': 2})

    assert_frame_equal(result, expected_output)


def test_fin_info_preparation():
    """
    Test the fin_info_preparation function with data containing irrelevant columns.
    """
    input_data = pd.DataFrame({
        "Ticker": ["AAPL", "GOOG"],
        "quoteType": ["Equity", "Equity"],
        "longName": ["Apple Inc.", "Alphabet Inc."],
        "shortName": ["Apple", "Alphabet"],
        "unrelatedColumn": [1, 2]
    })
    expected_output = pd.DataFrame({
        "Ticker": ["AAPL", "GOOG"],
        "quoteType": ["Equity", "Equity"],
        "longName": ["Apple Inc.", "Alphabet Inc."],
        "shortName": ["Apple", "Alphabet"]
    })

    result = fin_info_preparation(input_data)

    assert_frame_equal(result, expected_output)


def test_fin_ticker_preparation():
    """
    Test the fin_ticker_preparation function with a small dataset.
    """
    input_data = pd.DataFrame({
        "Ticker": ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN"]
    })
    exclude_tickers = pd.DataFrame({
        "Ticker": ["AAPL", "GOOG", "TSLA"]
    })
    expected_output = pd.DataFrame({
        "Ticker": ["MSFT", "AMZN"]
    })

    result = fin_ticker_preparation(input_data, exclude_tickers)

    assert_frame_equal(result, expected_output)
