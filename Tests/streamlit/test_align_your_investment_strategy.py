"""
This is a test file for the test_align_your_investment_strategy.py file.
"""
import pytest
import pandas as pd
from unittest.mock import patch
from Src.streamlit.align_your_investment_strategy import load_and_merge_data, get_unique_sectors_and_instruments, chunk_list


class MockDataLoader:
    def load_senators_trading(self):
        # Mocking the data returned by load_senators_trading
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOG', 'AMZN'],
            'sectorKey': ['Tech', 'Tech', 'Unknown'],
            'quoteType': ['Equity', 'Equity', 'Unknown'],
            'city': ['Cupertino', 'Mountain View', 'Seattle'],
            'country': ['USA', 'USA', 'USA']
        })

    def load_financial_instruments(self):
        # Mocking the data returned by load_financial_instruments
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOG', 'AMZN'],
            'industryKey': ['Tech', 'Tech', 'E-commerce'],
            'currency': ['USD', 'USD', 'USD'],
            'quoteType': ['Equity', 'Equity', 'Unknown'],
            'shortName': ['Apple', 'Google', 'Amazon'],
            'longName': ['Apple Inc.', 'Google Inc.', 'Amazon Inc.'],
            'financialCurrency': ['USD', 'USD', 'USD']
        })


@pytest.fixture
def mock_data_loader():
    # Fixture to use the mock DataLoader
    with patch('Src.scraping.scraper.DataLoader', MockDataLoader):
        yield


def test_load_and_merge_data():
    data_sector, data_instruments = load_and_merge_data()

    # Test function
    assert isinstance(data_sector, pd.DataFrame)
    assert isinstance(data_instruments, pd.DataFrame)
    assert 'Unknown' not in data_sector['sectorKey'].values
    assert 'Unknown' not in data_instruments['quoteType'].values
    required_columns_sector = ["Ticker", "sectorKey", "city", "country"]
    required_columns_instruments = ["Ticker", "quoteType", "currency", "shortName", "longName"]
    for col in required_columns_sector:
        assert col in data_sector.columns
    for col in required_columns_instruments:
        assert col in data_instruments.columns


@pytest.fixture
def sample_data():
    # Create mock data for instruments and sectors
    data_instruments = pd.DataFrame({
        "Politician": ["Politician1", "Politician2", "Politician3", "Politician4"],
        "quoteType": ["Equity", "Bond", "Equity", "Unknown"],
        "Transaction": ["Purchase", "Purchase", "Purchase", "Purchase"],
        "Invested": [1000, 2000, 1500, 3000]
    })
    data_sector = pd.DataFrame({
        "Politician": ["Politician1", "Politician2", "Politician3", "Politician4"],
        "sectorKey": ["Tech", "Finance", "Health", "Unknown"],
        "quoteType": ["EQUITY", "EQUITY", "EQUITY", "EQUITY"],
        "Transaction": ["Purchase", "Purchase", "Purchase", "Purchase"],
        "Invested": [1000, 2000, 1500, 3000]
    })
    return data_instruments, data_sector


def test_get_unique_sectors_and_instruments(sample_data):
    data_instruments, data_sector = sample_data

    # Test function
    list_of_unique_sectors, list_of_unique_instruments = get_unique_sectors_and_instruments(data_instruments, data_sector)
    assert sorted(list_of_unique_sectors) == ["Finance", "Health", "Tech"]
    assert sorted(list_of_unique_instruments) == ["Bond", "Equity"]


def test_chunk_list():
    lst = ["a", "b", "c", "d", "e", "f", "g"]

    # Test function
    result = list(chunk_list(lst, 3))
    expected_result = [["a", "b", "c"], ["d", "e", "f"], ["g"]]
    assert result == expected_result
    result_2 = list(chunk_list(lst, 2))
    expected_result_2 = [["a", "b"], ["c", "d"], ["e", "f"], ["g"]]
    assert result_2 == expected_result_2
    result_1 = list(chunk_list(lst, 1))
    expected_result_1 = [["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"]]
    assert result_1 == expected_result_1
