"""
This file contains the helper code for the Instrument Finder page.
"""
import streamlit as st
import pandas as pd
from Src.scraping.scraper import DataLoader


def instrument_information(data, selected_instrument):
    """
    Generates a summary of a financial instrument.

    Args:
        data (pd.DataFrame): Data containing instrument details with columns
            ['Ticker', 'city', 'country', 'industryKey', 'sectorKey',
             'longBusinessSummary', 'currency', 'quoteType', 'shortName',
             'longName', 'financialCurrency'].
        selected_instrument (str): The name of the instrument to describe.

    Returns:
        str: A descriptive summary of the instrument, omitting "Unknown" values.
    """
    # Filter the data
    data = data[data['Name'] == selected_instrument].iloc[0][
        ['Ticker', 'city', 'country', 'industryKey', 'sectorKey',
         'longBusinessSummary', 'currency', 'quoteType', 'shortName',
         'longName', 'financialCurrency']
    ]

    ticker, quote_type, short_name, long_name, location, sector, industry, currency, business_summary = "", "", "", "", "", "", "", "", ""

    if data['Ticker'] != "Unknown":
        ticker = f"The Financial instrument ticker is **{data['Ticker']}**."
    if data['quoteType'] != "Unknown":
        quote_type = f"It is a **{data['quoteType']}** fiancial instrument."
    if data['shortName'] != "Unknown":
        short_name = f"It is known as **{data['shortName']}**."
    if data['longName'] != "Unknown":
        long_name = f"The full name of the company is **{data['longName']}**"
    if data['city'] != "Unknown" and data['country'] != "Unknown":
        location = f"The company is located in **{data['city']}**, **{data['country']}**."
    if data['sectorKey'] != "Unknown":
        sector = f"The company operates in the **{data['sectorKey']}** sector."
    if data['industryKey'] != "Unknown":
        industry = f"The company's industry is **{data['industryKey']}**."
    if data['currency'] != "Unknown":
        currency = f"The company's currency is **{data['currency']}**."
    if data['longBusinessSummary'] != "Unknown":
        business_summary = f"\n\nThe company is involved in {data['longBusinessSummary']}."

    company_information = f"{ticker} {quote_type} {short_name} {long_name} {location} {sector} {industry} {currency} {business_summary}"

    return company_information


def market_gain(date, instrument):
    """
    Calculates the market gain for a given financial instrument from a specified date
    (adjusted to the first day of the month) to the current date.

    Args:
        date (str): The date string in the format 'YYYY-MM-DD'. The function will
                    adjust it to 'YYYY-MM-01' to align with monthly financial data.
        instrument (str): The ticker symbol of the financial instrument.

    Returns:
        float or str: The percentage gain from the specified date to the current
                      date. If an error occurs, returns "!unknown".
    """
    try:
        financial_data = DataLoader().load_financial_instruments()
        financial_data = financial_data[financial_data['Ticker'] == instrument]
        start_date = f"{date[:-2]}01"
        if start_date not in financial_data.columns:
            return "Unknown"

        buy_price = financial_data[start_date].values[0]
        current_price = financial_data[financial_data.columns.tolist()[-1]].values[0]

        gain = round(100 * ((current_price / buy_price) - 1), 2)

        return gain

    except Exception as e:
        st.error(f"Error processing {instrument}: {e}")
        return "Unknown"


def transform_data():
    """
    Function to load, filter, merge and transform senator trading data and financial instruments.
    Returns:
        list_of_instruments (numpy.ndarray): Sorted unique list of instrument names.
        data (pd.DataFrame): Transformed data containing merged information.
    """
    data_senators = DataLoader().load_senators_trading()
    data_instruments = DataLoader().load_financial_instruments()
    data_senators = data_senators[data_senators['Transaction'] == 'Purchase'].reset_index(drop=True)
    data = data_senators.merge(data_instruments, how="left", on="Ticker")
    data = data.fillna("Unknown")
    data["Name"] = data["Ticker"] + " - " + data["shortName"]
    list_of_instruments = data.Name.unique()
    list_of_instruments.sort()

    return list_of_instruments, data


def process_politician_data(instrument_data, politician):
    """
    Function to process the trading data for a given politician and return calculated results.
    Arguments:
    - instrument_data (pd.DataFrame): The dataframe containing all the instrument and trading data.
    - politician (str): The name of the politician whose trades need to be processed.

    Returns:
    - data_display (pd.DataFrame): Processed data to be displayed (with calculated columns for Gain, Profit, etc.)
    - weighted_profit (float): The weighted profit of the politician from their trades.
    - politician_data (pd.DataFrame): The original unprocessed data for the politician.
    """
    politician_data = instrument_data[instrument_data['Politician'] == politician].reset_index(drop=True)
    politician_data["Gain"] = politician_data.apply(lambda row: market_gain(row['Traded'], row['Ticker']), axis=1)
    politician_data['S&P 500'] = politician_data.apply(lambda row: market_gain(row['Traded'], "^GSPC"), axis=1)
    politician_data['Profit'] = (((politician_data['Gain'] / 100) + 1) * politician_data['Invested']).round(1)

    # Optimize DataFrame operations to avoid fragmentation
    data_display = pd.concat([
        politician_data[['Traded']],
        politician_data[['Invested']].map(lambda x: f"{x:,.2f} $"),
        politician_data[['Gain']].map(lambda x: f"{x:.2f} %"),
        politician_data[['Profit']].map(lambda x: f"{x:,.2f} $"),
        politician_data[['S&P 500']].map(lambda x: f"{x:.2f} %")
    ], axis=1)

    weighted_profit = round((politician_data['Invested'] * politician_data['Gain']).sum() / politician_data['Invested'].sum(), 2)

    return data_display, weighted_profit, politician_data
