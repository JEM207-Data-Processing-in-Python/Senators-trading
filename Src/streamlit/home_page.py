"""
This file contains the helper code for the Streamlit app's Home page.
"""
import pandas as pd

from Src.scraping.scraper import DataLoader


def general_information() -> tuple:
    """
    This function loads senator's trading data and returns key statistics:
    - Number of unique senators involved in trading.
    - Number of unique financial instruments (tickers) traded.
    - Total amount invested in purchase transactions.
    - Year of the first transaction made by a senator or last financial
    instrument update.

    Returns:
        tuple: (unique_politicians, unique_tickers, sum_invested,
        first_transaction)
    """
    # Load the data
    data_senators = DataLoader().load_senators_trading()
    data_financial = DataLoader().load_financial_instruments()

    # Check if data is empty
    if data_senators.empty:
        unique_politicians: str | int = "unknown"  # Can be "unknown" or an integer
        unique_tickers: str | int = "unknown"     # Can be "unknown" or an integer
        sum_invested = 0
        first_transaction = "unknown"
        last_update = "unknown"
    else:
        unique_politicians = len(data_senators['Politician'].unique())
        unique_tickers = len(data_senators['Ticker'].unique())
        sum_invested = data_senators[
            data_senators['Transaction'] == 'Purchase']['Invested'].sum()
        first_transaction = data_senators['Traded'].astype(
            'datetime64[ns]').min().strftime('%Y')
        last_update_fin = data_financial.columns[-1]
        last_update_sen = pd.to_datetime(
            data_senators['Filed'], errors='coerce').max().strftime('%Y-%m-%d')
        last_update = max(last_update_fin, last_update_sen)

    return unique_politicians, unique_tickers, sum_invested, first_transaction, last_update
