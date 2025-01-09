"""
Scraper functions for obtaining data from the internet - senators trading, financial instruments, and senators' information.
"""

import os
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import wikipedia
import yfinance as yf
import streamlit as st
from Src.scraping.scraper_utils import senators_data_preparation, fin_history_preparation, fin_info_preparation, fin_ticker_preparation


class DataLoader:
    def __init__(self):
        self.data_dir = "Data"

    def load_senators_trading(self):
        """
        Function that loads the senators trading dataset
        """
        return self._load_data("senators_trading.csv")

    def load_financial_instruments(self):
        """
        Function that loads the financial instruments dataset
        """
        return self._load_data("financial_instruments.csv")

    def load_senators_information(self):
        """
        Function that loads the senators information dataset
        """
        return self._load_data("senators_information.csv")

    def load_exclude_tickers(self):
        """
        Function that loads the excluded tickers dataset
        """
        return self._load_data("exclude_tickers.csv")

    def _load_data(self, filename):
        """
        Helper function to load a dataset from a CSV file
        """
        filepath = os.path.join(self.data_dir, filename)

        try:
            if os.path.exists(filepath):
                return pd.read_csv(filepath)
            else:
                raise FileNotFoundError(f"{filename} not found.")
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            if filename == "senators_trading.csv":
                Senators_Trading_Updater().update_senators_trading()
            elif filename == "financial_instruments.csv":
                Financial_Instruments_Updater().update_financial_instruments()
            elif filename == "senators_information.csv":
                Senators_Information_Updater().update_senators_information()
            elif filename == "exclude_tickers.csv":
                Financial_Instruments_Updater().update_financial_instruments()

            return pd.read_csv(filepath)


# TODO make the function more efficient and faster asynchronusly
class Senators_Trading_Updater:
    def __init__(self):
        self.data_loader = DataLoader()
        self.url = "https://trendspider.com/markets/wp-admin/admin-ajax.php"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def update_senators_trading(self):
        """
        Function that updates the senators trading dataset by iterating through the pages of the table on the website
        """
        try:
            current_data = self.data_loader.load_senators_trading()
            exclude_tickers = self.data_loader.load_exclude_tickers()
            last_current_data = self.get_last_current_data(current_data)
            page = 1
            new_data = []
            max_pages = 2
            progress_bar = st.progress(0)
            status_text = st.empty()

            while page <= max_pages:
                response = self.fetch_data(page)
                if response is None or response.status_code != 200:
                    print(f"Failed to fetch data: {response.status_code if response else 'No Response'}")
                    break

                response_json = response.json()
                html_content = response_json['table']
                max_pages = response_json['total_pages']
                soup = BeautifulSoup(html_content, 'html.parser')
                rows = soup.find_all('tr', class_='data-table__row')

                for row in rows:
                    row_data = self.extract_row_data(row, exclude_tickers)
                    if np.array_equal(last_current_data.values, row_data.values):
                        status_text.text("Found record already in dataset.")
                        current_data = pd.concat([pd.DataFrame(new_data), current_data], ignore_index=True)
                        status_text.text(f"Adding number of new records: {len(new_data)}")
                        current_data.to_csv(os.path.join("Data", "senators_trading.csv"), index=False)
                        return

                new_data.append(row_data)
                progress_percentage = min(page / max_pages, 1.0)
                progress_bar.progress(progress_percentage)
                status_text.text(f"Processing page {page}/{max_pages}")
                page += 1

            current_data = pd.concat([pd.DataFrame(new_data), current_data], ignore_index=True)
            status_text.text("Data saved to senators_trading.csv")
            current_data.to_csv(os.path.join("Data", "senators_trading.csv"), index=False)
            progress_bar.progress(1.0)
            status_text.text("All pages processed!")

        except Exception as e:
            print(f"An error occurred while updating senators trading data: {e}")

    def get_last_current_data(self, current_data):
        if current_data.empty:
            return pd.DataFrame(columns=['Ticker'])
        else:
            return current_data.iloc[0].to_frame().T.reset_index(drop=True)

    def fetch_data(self, page):
        data = {
            'action': 'get_congresstrading_table',
            'page': page,
            'limit': 10000,
            'politician': '',
            'ticker': ''
        }

        try:
            response = requests.post(self.url, data=data, headers=self.headers)
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            print(f"An error occurred while fetching data from the server: {e}")
            return None

    def extract_row_data(self, row, exclude_tickers):
        try:
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
            return senators_data_preparation(row_data, exclude_tickers)

        except AttributeError as e:
            print(f"An error occurred while extracting row data: {e}")
            return pd.DataFrame()


# TODO error handling, tests, make the function more efficient and faster asynchronusly
class Financial_Instruments_Updater:
    def __init__(self):
        self.data_loader = DataLoader()

    def update_financial_instruments(self):
        """
        Function that updates the financial instruments dataset with a progress bar.
        """
        current_data = self.data_loader.load_financial_instruments()
        senators_data = self.data_loader.load_senators_trading()
        exclude_tickers = self.data_loader.load_exclude_tickers()

        if current_data.empty:
            current_data = pd.DataFrame()

        tickers = senators_data.Ticker.drop_duplicates()
        tickers = fin_ticker_preparation(tickers, exclude_tickers)

        update_data = pd.DataFrame()
        total_tickers = len(tickers)
        progress_bar = st.progress(0)
        status_text = st.empty()
        i = 0

        for ticker in tickers:
            status_text.text(f"Processing ticker {ticker} ({i + 1}/{total_tickers})")
            print(f"{ticker} - {i}/{total_tickers}")
            progress_percentage = (i + 1) / total_tickers
            progress_bar.progress(progress_percentage)

            if self.is_data_up_to_date(current_data, ticker):
                i += 1
                continue

            symbol_info = self.get_symbol_info(ticker)
            if symbol_info is None:
                self.add_to_exclude_tickers(ticker, exclude_tickers)
                continue

            history = self.get_symbol_history(ticker)
            if history is None:
                self.add_to_exclude_tickers(ticker, exclude_tickers)
                continue

            symbol_info = pd.concat([symbol_info, history], axis=1)
            update_data = pd.concat([update_data, symbol_info], ignore_index=True)
            i += 1

        current_data = current_data[~current_data['Ticker'].isin(update_data['Ticker'])]
        current_data = pd.concat([current_data, update_data], ignore_index=True, join='outer')
        status_text.text("Data saved to financial_instruments.csv")
        current_data.to_csv(os.path.join("Data", "financial_instruments.csv"), index=False)
        progress_bar.progress(1.0)
        status_text.text("Update complete!")

    def is_data_up_to_date(self, current_data, ticker):
        calendar = USFederalHolidayCalendar()
        today = pd.Timestamp.today()
        custom_bday = pd.offsets.CustomBusinessDay(calendar=calendar)
        last_working_day = today - custom_bday

        return ticker in current_data["Ticker"].values and current_data[current_data["Ticker"] == ticker].columns[-1] == last_working_day.strftime('%Y-%m-%d')

    def get_symbol_info(self, ticker):
        symbol = yf.Ticker(ticker)
        symbol_info = pd.json_normalize(symbol.info).dropna(how='all', axis=1)
        symbol_info.insert(0, 'Ticker', ticker)
        symbol_info = fin_info_preparation(symbol_info)

        if 'quoteType' not in symbol_info.columns:
            return None

        return symbol_info

    def get_symbol_history(self, ticker):
        symbol = yf.Ticker(ticker)
        history = symbol.history(period="max").reset_index()

        if history.empty:
            return None

        return fin_history_preparation(history).set_index('Date').T.reset_index(drop=True)

    def add_to_exclude_tickers(self, ticker, exclude_tickers):
        if ticker not in exclude_tickers["Ticker"].values:
            exclude_tickers = pd.concat([exclude_tickers, pd.DataFrame({"Ticker": [ticker]})], ignore_index=True)
            exclude_tickers.to_csv(os.path.join("Data", "exclude_tickers.csv"), index=False)


class Senators_Information_Updater:
    def __init__(self):
        self.data_loader = DataLoader()

    def update_senators_information(self):
        """
        Function that updates the senators information dataset
        """
        current_data = self.data_loader.load_senators_information()
        senators_data = self.data_loader.load_senators_trading()

        if current_data.empty:
            current_data = pd.DataFrame()

        senators = senators_data.Politician.drop_duplicates()
        update_data = pd.DataFrame()
        disambiguation_errors = []
        i = 0

        for senator in senators:
            print(f"{senator} - {i}/{len(senators)}")
            chamber = senators_data.loc[senators_data["Politician"] == senator, "Chamber"].values[0]

            try:
                summary = wikipedia.summary(f"{senator} (US {chamber} politician)")
                page_url = wikipedia.page(f"{senator} (US {chamber} politician)").url

                if self._needs_update(current_data, senator, summary):
                    senator_info = self._create_senator_info(senator, summary, page_url, chamber)
                    update_data = pd.concat([update_data, senator_info], ignore_index=True)
                    i += 1

            except wikipedia.exceptions.DisambiguationError:
                print(f"Disambiguation error for {senator}. Skipping.")
                disambiguation_errors.append(senator)
                continue

        current_data = pd.concat([current_data, update_data], ignore_index=True, join='outer')
        print("Data saved to senators_information.csv")
        current_data.to_csv(os.path.join("Data", "senators_information.csv"), index=False)

        if disambiguation_errors:
            print("Disambiguation errors occurred for the following senators:")
            print(disambiguation_errors)

    def _needs_update(self, current_data, senator, summary):
        """Helper method to check if senator needs updating"""
        return (senator not in current_data["Politician"].values or current_data.loc[current_data["Politician"] == senator, "Information"].values[0] != summary)

    def _create_senator_info(self, senator, summary, page_url, chamber):
        """Helper method to create senator info DataFrame"""
        return pd.DataFrame([{
            "Politician": senator,
            "Information": summary,
            "Link": page_url,
            "Picture": wikipedia.page(f"{senator} (US {chamber} politician)").images[0]
        }])
