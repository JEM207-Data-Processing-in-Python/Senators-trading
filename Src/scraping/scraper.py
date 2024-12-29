"""
Scrapper functions for senators trading dataset and the financial inforamtion
"""
import pandas as pd
import numpy as np
import requests
import json
from pandas.tseries.holiday import USFederalHolidayCalendar
from bs4 import BeautifulSoup
import yfinance as yf
import scraper_utils as scrap_utils


# TODO error handling, tests, class
def load_senators_trading():
    """
    Function that loads the senators trading dataset
    """
    try:
        data = pd.read_csv(r"..\..\Data\senators_trading.csv")
    except FileNotFoundError:
        data = pd.DataFrame()

    return data


# TODO error handling, tests, class
def load_financial_instruments():
    """
    Function that loads the financial instruments dataset
    """
    try:
        data = pd.read_csv(r"..\..\Data\financial_instruments.csv")
    except FileNotFoundError:
        data = pd.DataFrame()

    return data


# TODO error handling, tests, make the function more efficient and faster asynchronusly, class
def update_senators_trading(current_data):
    """
    Function that updates the senators trading dataset by iterating through the pages of the table on the website
    """
    # obtain last trade record curerntly in the dataset
    if current_data.empty:
        last_current_data = pd.DataFrame()
    else:
        last_current_data = current_data.iloc[0].to_frame().T.reset_index(drop=True)

    # URL of the website
    url = "https://trendspider.com/markets/wp-admin/admin-ajax.php"

    # Headers sent to the POST request
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # Variables for the loop
    page = 1
    new_data = pd.DataFrame()
    max_pages = 2

    while page != max_pages:
        # Data sent in the POST request
        data = {
            'action': 'get_congresstrading_table',
            'page': page,
            'limit': 10000,
            'politician': '',
            'ticker': ''
        }

        # Send POST request with headers
        response = requests.post(url, data=data, headers=headers)

        # Check if the data was fetched successfully
        if response.status_code == 200:
            print("Connection established")
        else:
            print(f"Failed to fetch data: {response.status_code}")

        # Parse the JSON response
        response_json = json.loads(response.content.decode('utf-8'))
        html_content = response_json['table']
        max_pages = response_json['total_pages']
        print(f"Page {page}/{max_pages}")
        soup = BeautifulSoup(html_content, 'html.parser')
        rows = soup.find_all('tr', class_='data-table__row')

        # Extract the data from the page
        for row in rows:
            ticker = row.select_one('td[data-title="Stock"]').contents[0].strip()
            politician = row.select_one('td[data-title="Politician"] a').text.strip()
            party = row.select_one('td[data-title="Politician"] abbr').text.strip()
            chamber = row.select_one('td[data-title="Politician"] div small').contents[-1].strip()
            transaction = row.select_one('td[data-title="Transaction"] span').text.strip().split()[0]
            amount = row.select_one('td[data-title="Transaction"] div small').text.strip()
            traded_date = row.select_one('td[data-title="Traded"] div').text.strip()
            filed_date = row.select_one('td[data-title="Filed"] div').text.strip()
            row_data = pd.DataFrame([{
                'Ticker': ticker,
                'Politician': politician,
                'Party': party,
                'Chamber': chamber,
                'Transaction': transaction,
                'Amount': amount,
                'Traded Date': traded_date,
                'Filed Date': filed_date
            }])
            row_data = scrap_utils.senators_data_preparation(row_data)

            if np.array_equal(last_current_data.values, row_data.values):
                print("Found record already in dataset.")
                current_data = pd.concat([new_data, current_data], ignore_index=True)
                print("Adding number of new recors: ",len(new_data))
                current_data.to_csv(r"..\..\Data\senators_trading.csv", index = False)
                return

            new_data = pd.concat([new_data, row_data], ignore_index=True)
            print(len(new_data))

        page += 1
    current_data = pd.concat([new_data, current_data], ignore_index=True)
    print("Data saved to senators_trading.csv")
    current_data.to_csv(r"..\..\Data\senators_trading.csv", index = False)

    return

#update_senators_trading(load_senators_trading())

# TODO error handling, tests, make the function more efficient and faster asynchronusly, class
def update_financial_instruments(current_data, senators_data):
    """
    Function that updates the financial instruments dataset
    """
    # obtain all tickers that are already in dataset
    if current_data.empty:
        curent_data = pd.DataFrame()

    tickers = senators_data.Ticker.drop_duplicates()
    tickers = scrap_utils.fin_ticker_preparation(tickers)

    # Create empty dataframes for each type of asset
    update_data = pd.DataFrame()
    i=0
    # Get the information about the assets
    for ticker in tickers:
        # Check if the data is up to date
        print(f"{ticker} - {i}/{len(tickers)}")
        calendar = USFederalHolidayCalendar()
        today = pd.Timestamp.today()
        custom_bday = pd.offsets.CustomBusinessDay(calendar=calendar)
        last_working_day = today - custom_bday

        # Check if the ticker is already in the dataset and have last trade record
        if ticker in current_data["Ticker"].values and current_data[current_data["Ticker"] == ticker].columns[-1] == last_working_day.strftime('%Y-%m-%d'):
            i+=1
            continue

        # Get the information about the asset
        symbol = yf.Ticker(ticker)
        symbol_info = pd.json_normalize(symbol.info)
        symbol_info = symbol_info.dropna(how='all', axis=1)
        symbol_info.insert(0, 'Ticker', ticker)
        symbol_info = scrap_utils.fin_info_preparation(symbol_info)

        # Check if the asset has the necessary information
        if 'quoteType' not in symbol_info.columns or symbol.history(period="max").empty:
            print(f"No information found for {ticker}.")
            continue

        history = scrap_utils.fin_history_preparation(symbol.history(period="max").reset_index()).set_index('Date').T
        history.reset_index(drop=True, inplace=True)

        symbol_info = pd.concat([symbol_info, history], axis=1)
        update_data = pd.concat([update_data, symbol_info], ignore_index=True)
        i+=1

    current_data = current_data[~current_data['Ticker'].isin(update_data['Ticker'])]
    current_data = pd.concat([current_data, update_data], ignore_index=True, join='outer')
    print("Data saved to financial_instruments.csv")
    current_data.to_csv(r"..\..\Data\financial_instruments.csv", index=False)

    return

#update_financial_instruments(load_financial_instruments(), load_senators_trading())
