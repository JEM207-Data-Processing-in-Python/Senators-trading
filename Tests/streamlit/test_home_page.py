"""
This file contains the Test cases for the home_page.py file.
"""
import pytest
import pandas as pd

from Src.scraping.scraper import DataLoader
from Src.streamlit.home_page import general_information


class MockDataLoader:
    def load_senators_trading(self):
        data = {
            'Politician': ['Senator A', 'Senator B', 'Senator A'],
            'Ticker': ['AAPL', 'GOOGL', 'AAPL'],
            'Transaction': ['Purchase', 'Purchase', 'Purchase'],
            'Invested': [1000, 2000, 1500],
            'Traded': ['2022-01-01', '2023-05-15', '2021-03-22'],
            'Filed': ['2023-01-01', '2023-02-15', '2023-05-10'],
        }
        return pd.DataFrame(data)

    def load_financial_instruments(self):
        return pd.DataFrame({
            'AAPL': ['2022-01-01'],
            'GOOGL': ['2022-01-01'],
            'AMZN': ['2022-01-01'],
            'Last_Update': ['2023-03-01']
        })


@pytest.fixture
def mock_data_loader(monkeypatch):
    monkeypatch.setattr(DataLoader, 'load_senators_trading', MockDataLoader().load_senators_trading)
    monkeypatch.setattr(DataLoader, 'load_financial_instruments', MockDataLoader().load_financial_instruments)


def test_general_information(mock_data_loader):
    # Test function
    unique_politicians, unique_tickers, sum_invested, first_transaction, last_update = general_information()

    assert unique_politicians == 2
    assert unique_tickers == 2
    assert sum_invested == 4500
    assert first_transaction == '2021'
    assert last_update == 'Last_Update'
