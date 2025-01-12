"""
This is a test file for the scraper_utils_1.py file.
"""

import pytest
import pandas as pd
from Src.scraping.scraper_utils_1 import load_data, get_last_current_data, delete_exclude_tickers, senators_data_preparation


def test_load_data_existing_file(tmpdir):
    filepath = tmpdir.join("test_data.csv")
    columns = ['col1', 'col2']
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    df.to_csv(str(filepath), index=False)

    # Test function
    loaded_df = load_data(str(filepath), columns)
    assert not loaded_df.empty
    assert list(loaded_df.columns) == columns


def test_load_data_non_existing_file(tmpdir):
    filepath = tmpdir.join("non_existing_file.csv")
    columns = ['col1', 'col2']

    # Test function
    df = load_data(str(filepath), columns)
    assert df.empty
    assert list(df.columns) == columns


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
