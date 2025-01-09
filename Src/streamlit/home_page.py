"""
This file contains the helper code for the Streamlit app's Home page.
"""

from Src.scraping.scraper import DataLoader

def general_information() -> tuple:
    """
    This function loads senator's trading data and returns key statistics:
    - Number of unique senators involved in trading.
    - Number of unique financial instruments (tickers) traded.
    - Total amount invested in purchase transactions.
    - Year of the first transaction made by a senator.

    Returns:
        tuple: (unique_politicians, unique_tickers, sum_invested, first_transaction)
    """
    # Load the data
    data_senators = DataLoader().load_senators_trading()

    # Calculate statistics
    unique_politicians = len(data_senators['Politician'].unique())
    unique_tickers = len(data_senators['Ticker'].unique())
    sum_invested = data_senators[data_senators['Transaction'] == 'Purchase']['Invested'].sum()
    first_transaction = data_senators['Traded'].astype('datetime64[ns]').min().strftime('%Y')

    return unique_politicians, unique_tickers, sum_invested, first_transaction
