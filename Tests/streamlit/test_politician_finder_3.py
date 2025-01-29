"""
This file contains the tests for the politician_finder_3.py file.
"""
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from Src.streamlit.politician_finder_3 import wikipedia_information, chamber_politician, individual_invest_politician, most_active_sell, most_active_purchase


@patch("Src.scraping.scraper.DataLoader")
def test_wikipedia_information_not_found(mock_data_loader_class):
    mock_data_loader = MagicMock()
    mock_data_loader_class.return_value = mock_data_loader
    mock_data_loader.load_senators_information.return_value = pd.DataFrame(columns=["Politician", "Information", "Link", "Picture"])

    # Test function
    information, link, picture = wikipedia_information("Nonexistent Politician")
    assert information is None
    assert link is None
    assert picture is None


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Politician': ['John Doe', 'Jane Smith', 'Mark Lee'],
        'Chamber': ['House', 'Senate', 'House']
    })


def test_chamber_politician_found_house(sample_data):
    result = chamber_politician(sample_data, 'John Doe')
    assert result == 'House of Representatives', "Should return 'House of Representatives'"


def test_chamber_politician_found_senate(sample_data):
    result = chamber_politician(sample_data, 'Jane Smith')
    assert result == 'Senate', "Should return 'Senate'"


data = pd.DataFrame({
    'shortName': ['StockA', 'StockB', 'StockC'],
    'Invested': [1000, 2000, 3000],
    'Ticker': ['A', 'B', 'C'],
    'quoteType': ['Type1', 'Type1', 'Type2'],
    'Transaction': ['Purchase', 'Purchase', 'Purchase'],
    'Politician': ['Politician1', 'Politician1', 'Politician1'],
    'Traded': ['2013-01-01', '2013-01-01', '2013-01-01']
})


def mocked_top_five_purchased_stocks(data, selected_politician, quoteType):
    return data[(data['Politician'] == selected_politician) & (data['quoteType'] == quoteType)]


@patch('Src.visualization.tables.top_five_purchased_stocks', side_effect=mocked_top_five_purchased_stocks)
def test_individual_invest_politician(mock_top_five):
    selected_politician = 'Politician1'
    quote_types = ['Type1', 'Type2']
    expected_message = (
        "in Type1, where the most popular investment is StockB with a total amount invested of 2 000 USD;"
        " in Type2, where the most popular investment is StockC with a total amount invested of 3 000 USD"
    )

    # Test function
    result = individual_invest_politician(data, quote_types, selected_politician)
    assert result == expected_message


@pytest.fixture
def mock_data():
    return pd.DataFrame({
        'Politician': ['Politician A', 'Politician A', 'Politician B', 'Politician A'],
        'Transaction': ['Sale', 'Sale', 'Sale', 'Sale'],
        'Traded': ['Stock1', 'Stock2', 'Stock1', 'Stock1'],
        'Invested': [-500, -200, -300, -1000],
        'quoteType': ['EQUITY', 'BOND', 'EQUITY', 'EQUITY'],
        'sector': ['Tech', 'Finance', 'Tech', 'Energy']
    })


def test_no_sales(mock_data):
    # Test function
    result = most_active_sell(mock_data, 'Politician C')
    assert result == "Politician C has not sold any instruments during the documented period."


def test_most_active_sale(mock_data):
    # Test function
    result = most_active_sell(mock_data, 'Politician A')
    assert "Politician A sold the most on Stock1" in result
    assert "with a total volume sold of 1,500 USD." in result


def create_sample_data():
    return pd.DataFrame({
        'Politician': ['Politician A', 'Politician A', 'Politician B', 'Politician A'],
        'Transaction': ['Purchase', 'Purchase', 'Purchase', 'Purchase'],
        'Traded': ['2025-01-01', '2025-01-02', '2025-01-01', '2025-01-03'],
        'Invested': [10000, 5000, 15000, 20000],
        'quoteType': ['Stock A', 'Stock B', 'Stock A', 'Stock C']
    })


def test_most_active_purchase_with_data():
    data = create_sample_data()

    # Test function
    result = most_active_purchase(data, 'Politician A')
    assert 'Politician A' in result
    assert 'invested the most on day' in result
    assert 'The most purchased stock type is' in result


def test_most_active_purchase_no_data():
    # Test function
    data = create_sample_data()
    result = most_active_purchase(data, 'Politician C')
    assert 'has not purchased any instruments' in result


def test_most_active_purchase_tie():
    data = pd.DataFrame({
        'Politician': ['Politician A', 'Politician A', 'Politician A'],
        'Transaction': ['Purchase', 'Purchase', 'Purchase'],
        'Traded': ['2025-01-01', '2025-01-02', '2025-01-03'],
        'Invested': [10000, 10000, 5000],
        'quoteType': ['Stock A', 'Stock B', 'Stock A']
    })

    # Test function
    result = most_active_purchase(data, 'Politician A')
    assert 'invested the most on day' in result
