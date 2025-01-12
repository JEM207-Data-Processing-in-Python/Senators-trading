"""
This file contains the the Tests for politician_finder_2.py file.
"""
import pytest
import pandas as pd
from Src.streamlit.politician_finder_2 import most_trade_type_politician, most_traded_volume_politician, most_traded_sector_politician, most_sold_sector_politician


@pytest.fixture
def sample_data():
    data = {
        "Politician": ["John Doe", "Jane Smith", "John Doe", "Jane Smith", "John Doe", "Jane Sold"],
        "Transaction": ["Purchase", "Purchase", "Purchase", "Sale", "Purchase", "Sale"],
        "quoteType": ["EQUITY", "BOND", "EQUITY", "EQUITY", "EQUITY", "EQUITY"],
        "sectorKey": ["Tech", "Finance", "Tech", "Energy", "Tech", "Tech"],
        "Invested": [1000, 1500, 2000, 500, 3000, 2000]
    }
    return pd.DataFrame(data)


def test_most_trade_type_politician(sample_data):
    # John Doe is the selected politician
    result = most_trade_type_politician(sample_data, "John Doe")
    assert "John Doe invests the most often into EQUITY" in result


def test_most_trade_type_politician_no_purchase(sample_data):
    # Test function
    result = most_trade_type_politician(sample_data, "Jane Sold")
    assert "Jane Sold has not performed any purchases" in result


def test_most_traded_volume_politician(sample_data):
    # Test function
    result = most_traded_volume_politician(sample_data, "John Doe")
    assert "with the total average amount purchased of 6,000 USD" in result


def test_most_traded_volume_politician_no_purchase(sample_data):
    # Test function
    result = most_traded_volume_politician(sample_data, "Jane Sold")
    assert result == ""


def test_most_traded_sector_politician(sample_data):
    # Test function
    result = most_traded_sector_politician(sample_data, "John Doe")
    assert "When it comes to EQUITY, this politician mostly invests in Tech" in result


def test_most_traded_sector_politician_no_equity(sample_data):
    # Test function
    sample_data_no_equity = sample_data[sample_data["quoteType"] != "EQUITY"]
    result = most_traded_sector_politician(sample_data_no_equity, "Jane Smith")
    assert "They have not invested in EQUITY either." in result


def test_most_sold_sector_politician(sample_data):
    # Test function
    result = most_sold_sector_politician(sample_data, "Jane Smith")
    assert "Jane Smith sold EQUITY mostly in Energy sector with the total average volume sold of -500 USD." in result


def test_most_sold_sector_politician_no_sale(sample_data):
    # Test function
    sample_data_no_sale = sample_data[sample_data["Transaction"] != "Sale"]
    result = most_sold_sector_politician(sample_data_no_sale, "John Doe")
    assert "They did not perform any sales of EQUITY during the documented time period." in result
