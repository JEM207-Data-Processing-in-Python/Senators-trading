"""
This file contains the tests for the tables.py file.
"""
import pandas as pd
import pytest

from Src.visualization.tables import top_five_purchased_stocks, top_five_sold_stocks, data_for_strategy_align_type, data_for_strategy_align_sector


@pytest.fixture
def mock_data():
    data = {
        "Politician": ["John Doe", "John Doe", "Jane Smith", "John Doe", "John Doe", "Jane Smith"],
        "quoteType": ["EQUITY", "EQUITY", "EQUITY", "BOND", "EQUITY", "EQUITY"],
        "Transaction": ["Purchase", "Purchase", "Purchase", "Purchase", "Purchase", "Sell"],
        "Invested": [1000, 2000, 1500, 3000, 2500, 1200],
        "Ticker": ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "AAPL"],
        "shortName": ["Apple", "Google", "Microsoft", "Tesla", "Amazon", "Apple"],
        "sectorKey": ["Tech", "Tech", "Tech", "Auto", "Retail", "Tech"],
        "Traded": ["2024-01-10", "2024-01-11", "2024-01-12", "2024-01-09", "2024-01-13", "2024-01-08"],
    }
    df = pd.DataFrame(data)
    df["Traded"] = pd.to_datetime(df["Traded"])
    return df


def test_top_five_purchased_stocks_non_equity(mock_data):
    # Test function
    result = top_five_purchased_stocks(mock_data, politician="John Doe", quoteType="BOND")
    assert isinstance(result, pd.DataFrame)
    assert result.index.tolist() == ["TSLA"]
    assert "Total Invested" in result.columns
    assert "Last Purchase" in result.columns
    assert result.loc["TSLA", "Total Invested"] == "3 000 USD"


def test_top_five_purchased_stocks_no_data(mock_data):
    # Test function
    result = top_five_purchased_stocks(mock_data, politician="Unknown Politician", quoteType="EQUITY")
    assert result.empty


def test_top_five_purchased_stocks_equity(mock_data):
    # Test function
    result = top_five_purchased_stocks(mock_data, politician="John Doe", quoteType="EQUITY")
    assert isinstance(result, pd.DataFrame), "The result should be a pandas DataFrame."
    assert result.index.tolist() == ["AMZN", "GOOG", "AAPL"], "The tickers should be sorted by total invested."
    assert "Total Invested" in result.columns, "The result should include a 'Total Invested' column."
    assert "Last Purchase" in result.columns, "The result should include a 'Last Purchase' column."
    assert result.loc["AMZN", "Total Invested"] == "2 500 USD", "The total invested for AMZN should be '2 500 USD'."


def test_top_five_sold_stocks_no_data(mock_data):
    politician = "Nonexistent Politician"
    quoteType = "EQUITY"

    # Test function
    result = top_five_sold_stocks(mock_data, politician, quoteType)
    assert result.empty, "The result should be empty for unmatched filters."


def test_top_five_sold_stocks_non_equity(mock_data):
    """Test top_five_sold_stocks for non-EQUITY quoteType."""
    politician = "John Doe"
    quoteType = "BOND"

    # Test function
    result = top_five_sold_stocks(mock_data, politician, quoteType)
    assert result.empty, "The result should be empty as there are no 'Sale' transactions for BOND."


def test_top_five_sold_stocks_missing_sale(mock_data):
    politician = "John Doe"
    quoteType = "EQUITY"

    # Test function
    result = top_five_sold_stocks(mock_data, politician, quoteType)
    assert result.empty, "The result should be empty as there are no 'Sale' transactions for this politician."


def test_data_for_strategy_align_type(mock_data):
    # Test function
    result = data_for_strategy_align_type(mock_data)
    expected_output = pd.DataFrame({
        "Politician": ["Jane Smith", "Jane Smith", "John Doe", "John Doe"],
        "quoteType": ["BOND", "EQUITY", "BOND", "EQUITY"],
        "Total Invested Type": [0.0, 100.0, 35.294117647058826, 64.70588235294117],
        "Total Invested": [0.0, 1500.0, 8500.0, 8500.0],
    })
    result = result.sort_values(by=["Politician", "quoteType"]).reset_index(drop=True)
    expected_output = expected_output.sort_values(by=["Politician", "quoteType"]).reset_index(drop=True)

    pd.testing.assert_frame_equal(result, expected_output, check_exact=False, atol=1e-6)


def create_sample_data():
    return pd.DataFrame({
        "Politician": ["A", "A", "B", "B", "C", "C"],
        "sectorKey": ["Tech", "Finance", "Tech", "Finance", "Energy", "Tech"],
        "quoteType": ["EQUITY", "EQUITY", "EQUITY", "EQUITY", "EQUITY", "EQUITY"],
        "Transaction": ["Purchase", "Purchase", "Purchase", "Purchase", "Purchase", "Purchase"],
        "Invested": [100, 200, 150, 50, 300, 100]
    })


def test_data_for_strategy_align_sector():
    data = create_sample_data()

    # Test function
    result = data_for_strategy_align_sector(data)
    assert isinstance(result, pd.DataFrame), "Output should be a DataFrame."
    assert "Politician" in result.columns, "Output should contain 'Politician' column."
    assert "sectorKey" in result.columns, "Output should contain 'sectorKey' column."
    assert "Total Invested Sector" in result.columns, "Output should contain 'Total Invested Sector' column."
    assert not result.empty, "Output DataFrame should not be empty."


def test_empty_data():
    data = pd.DataFrame(columns=["Politician", "sectorKey", "quoteType", "Transaction", "Invested"])

    # Test function
    result = data_for_strategy_align_sector(data)
    assert isinstance(result, pd.DataFrame), "Output should be a DataFrame."
    assert result.empty, "Output DataFrame should be empty when input data is empty."
