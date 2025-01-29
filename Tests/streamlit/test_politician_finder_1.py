"""
This file contains the Test cases for the politician_finder_1.py file.
"""
import pytest
import pandas as pd
from Src.streamlit.politician_finder_1 import party_politician, first_trade_politician, last_trade_politician, total_invested_politician, total_sold_politician


@pytest.fixture
def sample_data():
    data = {
        "Politician": ["John Doe", "Jane Smith", "John Doe", "Jane Smith"],
        "Party": ["R", "D", "R", "D"],
        "Traded": ["2021-05-01", "2022-03-15", "2023-01-25", "2024-07-19"],
        "Transaction": ["Purchase", "Sale", "Purchase", "Sale"],
        "Invested": [5000, 2000, 15000, 3000],
    }
    return pd.DataFrame(data)


def test_party_politician(sample_data):
    # Test function
    assert party_politician(sample_data, "John Doe") == "Republican Party"
    assert party_politician(sample_data, "Jane Smith") == "Democratic Party"


def test_first_trade_politician(sample_data):
    # Test function
    assert first_trade_politician(sample_data, "John Doe") == "2021-05-01"
    assert first_trade_politician(sample_data, "Jane Smith") == "2022-03-15"


def test_last_trade_politician(sample_data):
    # Test function
    assert last_trade_politician(sample_data, "John Doe") == "2023-01-25"
    assert last_trade_politician(sample_data, "Jane Smith") == "2024-07-19"


def test_total_invested_politician(sample_data):
    # Test function
    assert total_invested_politician(sample_data, "John Doe") == "20,000"
    assert total_invested_politician(sample_data, "Jane Smith") == "0"


def test_total_sold_politician(sample_data):
    # Test function
    assert total_sold_politician(sample_data, "John Doe") == "0"
    assert total_sold_politician(sample_data, "Jane Smith") == "-5,000"
