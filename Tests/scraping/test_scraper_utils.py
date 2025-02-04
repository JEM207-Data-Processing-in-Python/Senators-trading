"""
This is a test file for the scraper_utils.py file.
"""

import pytest
import pandas as pd

from Src.scraping.scraper_utils import (
    get_last_current_data, delete_exclude_tickers,
    senators_data_preparation, fin_history_preparation,
    fin_info_preparation, fin_ticker_preparation,
    is_data_up_to_date, add_to_exclude_tickers,
    get_profile_picture
)


def test_get_last_current_data_empty():
    df = pd.DataFrame(columns=['col1', 'col2'])

    # Test function
    result = get_last_current_data(df)
    assert result is None


def test_get_last_current_data_non_empty():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    # Test function
    result = get_last_current_data(df)
    assert result is not None
    assert result.shape[0] == 1
    assert result.iloc[0]['col1'] == 1
    assert result.iloc[0]['col2'] == 3


@pytest.fixture
def sample_data():
    # Sample data for current_data DataFrame
    return pd.DataFrame({
        'Ticker': ['AAPL', 'GOOG', 'AMZN', 'TSLA', 'MSFT'],
        'Price': [150, 2800, 3400, 700, 280]
    })


@pytest.fixture
def exclude_data():
    # Sample data for exclude_tickers DataFrame
    return pd.DataFrame({
        'Ticker': ['GOOG', 'MSFT']
    })


def test_delete_exclude_tickers(sample_data, exclude_data):
    # Test function
    result = delete_exclude_tickers(exclude_data, sample_data)
    expected = pd.DataFrame({
        'Ticker': ['AAPL', 'AMZN', 'TSLA'],
        'Price': [150, 3400, 700]
    })
    result_reset = result.reset_index(drop=True)
    expected_reset = expected.reset_index(drop=True)
    pd.testing.assert_frame_equal(result_reset, expected_reset)


def test_senators_data_preparation():
    input_data = pd.DataFrame({
        'Transaction': ['Purchase', 'Sale'],
        'Amount': ['$1,000 - $15,000', '$5,000 - $10,000'],
        'Ticker': ['AAPL', 'GOOGL'],
        'Traded Date': ['Jan 15, 2023', 'Feb 20, 2023'],
        'Filed Date': ['Jan 20, 2023', 'Feb 25, 2023']
    })
    exclude_tickers = pd.DataFrame({
        'Ticker': ['TESLA', 'META']
    })

    expected_output = pd.DataFrame({
        'Transaction': ['Purchase', 'Sale'],
        'Ticker': ['AAPL', 'GOOGL'],
        'Traded': ['2023-01-15', '2023-02-20'],
        'Filed': ['2023-01-20', '2023-02-25'],
        'Invested': [8000.0, -7500.0]
    })

    # Test function
    result = senators_data_preparation(input_data, exclude_tickers)
    pd.testing.assert_frame_equal(result.reset_index(drop=True),
                                  expected_output.reset_index(drop=True))


def test_senators_data_preparation_with_exclusions():
    input_data = pd.DataFrame({
        'Transaction': ['Purchase', 'Purchase'],
        'Amount': ['$1,000 - $15,000', '$5,000 - $10,000'],
        'Ticker': ['AAPL', 'TESLA'],
        'Traded Date': ['Jan 15, 2023', 'Feb 20, 2023'],
        'Filed Date': ['Jan 20, 2023', 'Feb 25, 2023']
    })
    exclude_tickers = pd.DataFrame({
        'Ticker': ['TESLA', 'META']
    })
    expected_output = pd.DataFrame({
        'Transaction': ['Purchase'],
        'Ticker': ['AAPL'],
        'Traded': ['2023-01-15'],
        'Filed': ['2023-01-20'],
        'Invested': [8000.0]
    })

    # Test function
    result = senators_data_preparation(input_data, exclude_tickers)
    pd.testing.assert_frame_equal(result.reset_index(drop=True),
                                  expected_output.reset_index(drop=True))


def test_senators_data_preparation_invalid_data():
    input_data = pd.DataFrame({
        'Transaction': ['Purchase'],
        'Amount': ['$1,000 - $15,000'],
        'Ticker': ['AAPL'],
        'Traded Date': ['Invalid Date'],
        'Filed Date': ['Jan 20, 2023']
    })
    exclude_tickers = pd.DataFrame({
        'Ticker': ['TESLA']
    })

    # Test function
    with pytest.raises(Exception):
        senators_data_preparation(input_data, exclude_tickers)


def test_senators_data_preparation_long_ticker():
    input_data = pd.DataFrame({
        'Transaction': ['Purchase'],
        'Amount': ['$1,000 - $15,000'],
        'Ticker': ['TOOLONG'],
        'Traded Date': ['Jan 15, 2023'],
        'Filed Date': ['Jan 20, 2023']
    })

    exclude_tickers = pd.DataFrame({
        'Ticker': ['TESLA']
    })
    expected_output = pd.DataFrame({
        'Transaction': [],
        'Ticker': [],
        'Traded': [],
        'Filed': [],
        'Invested': []
    })

    # Test function
    result = senators_data_preparation(input_data, exclude_tickers)
    assert len(result) == 0
    assert all(col in result.columns for col in expected_output.columns)


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
