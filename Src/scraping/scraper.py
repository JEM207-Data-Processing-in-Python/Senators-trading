"""
Scraper functions for obtaining data from the internet - senators trading,
financial instruments, and senators' information.
"""
import os
import time
import logging
from multiprocessing import Pool

import requests
from requests.exceptions import RequestException
import numpy as np
import pandas as pd
import wikipedia
import yfinance as yf
import streamlit as st
from bs4 import BeautifulSoup

from Src.scraping.scraper_utils import (
    load_data, get_last_current_data, delete_exclude_tickers,
    senators_data_preparation, fin_history_preparation,
    fin_info_preparation, fin_ticker_preparation,
    is_data_up_to_date, add_to_exclude_tickers,
    get_profile_picture
)

# Suppress streamlit logs
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context")\
    .setLevel(logging.ERROR)
logging.getLogger("streamlit").setLevel(logging.CRITICAL)


class DataLoader:
    def __init__(self):
        self.data_dir = "Data"
        os.makedirs(self.data_dir, exist_ok=True)

    def load_senators_trading(self):
        """
        Function that loads the senators trading dataset
        """
        filepath = os.path.join(self.data_dir, "senators_trading.csv")
        return load_data(filepath, columns=["Ticker"])

    def load_financial_instruments(self):
        """
        Function that loads the financial instruments dataset
        """
        filepath = os.path.join(self.data_dir, "financial_instruments.csv")
        return load_data(filepath, columns=["Ticker"])

    def load_senators_information(self):
        """
        Function that loads the senators information dataset
        """
        filepath = os.path.join(self.data_dir, "senators_information.csv")
        return load_data(filepath, columns=["Politician"])

    def load_exclude_tickers(self):
        """
        Function that loads the excluded tickers dataset
        """
        filepath = os.path.join(self.data_dir, "exclude_tickers.csv")
        return load_data(filepath, columns=["Ticker"])


class Senators_Trading_Updater:
    def __init__(self):
        self.data_loader = DataLoader()
        self.url = "https://trendspider.com/markets/wp-admin/admin-ajax.php"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def update_senators_trading(self):
        """
        Function that updates the senators trading dataset by iterating through
        the pages of the table on the website.
        """
        try:
            current_data = self.data_loader.load_senators_trading()
            exclude_tickers = self.data_loader.load_exclude_tickers()
            last_current_data = get_last_current_data(current_data)
            page = 1
            new_data = pd.DataFrame()
            max_pages = 2
            progress_bar = st.progress(0)
            status_text = st.empty()

            if current_data.empty:
                current_data = pd.DataFrame(columns=['Ticker'])

            while page <= max_pages:
                response = self.fetch_data(page)

                if response is None or response.status_code != 200:
                    status_text.text(
                        f"Failed to fetch data from table: "
                        f"{response.status_code if response else 'No Response'}"
                    )
                    break

                response_json = response.json()
                html_content = response_json['table']
                max_pages = response_json['total_pages']
                soup = BeautifulSoup(html_content, 'html.parser')
                rows = soup.find_all('tr', class_='data-table__row')
                progress_bar.progress(min(page / max_pages, 1.0))
                status_text.text(
                    f"Processing batch {page}/{max_pages}, each batch contains "
                    "10000 records."
                )

                for row in rows:
                    row_data = self.extract_row_data(row, exclude_tickers)
                    new_data = pd.concat([new_data, row_data], ignore_index=True)

                    if np.array_equal(last_current_data.values, row_data.values):
                        status_text.text(
                            "Encountered record that we have already in the "
                            "dataset."
                        )
                        progress_bar.progress(100)
                        new_data = new_data.iloc[:-1]
                        current_data = pd.concat(
                            [new_data, current_data], ignore_index=True
                        )
                        current_data = delete_exclude_tickers(
                            exclude_tickers, current_data
                        )
                        time.sleep(2)
                        status_text.text(
                            f"All {len(new_data)} new records from the internet "
                            "loaded successfully and saved to senators_trading.csv"
                        )
                        current_data.to_csv(
                            os.path.join("Data", "senators_trading.csv"),
                            index=False
                        )
                        return None

                page += 1

            current_data = pd.concat([new_data, current_data], ignore_index=True)
            current_data = delete_exclude_tickers(exclude_tickers, current_data)
            progress_bar.progress(100)
            status_text.text(
                f"All {len(new_data)} new records from the internet saved to "
                "senators_trading.csv"
            )
            current_data.to_csv(
                os.path.join("Data", "senators_trading.csv"), index=False
            )

        except Exception as e:
            logging.error(
                f"An error occurred while updating senators trading data: {e}"
            )

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
            logging.error(
                f"An error occurred while fetching data from the server: {e}"
            )
            return None

    def extract_row_data(self, row, exclude_tickers):
        try:
            ticker = row.select_one('td[data-title="Stock"]').contents[0].strip()
            politician = row.select_one('td[data-title="Politician"] a').text.strip()
            party = row.select_one('td[data-title="Politician"] abbr').text.strip()
            chamber = row.select_one('td[data-title="Politician"] div small')\
                .contents[-1].strip()
            transaction = row.select_one('td[data-title="Transaction"] span')\
                .text.strip().split()[0]
            amount = row.select_one('td[data-title="Transaction"] div small')\
                .text.strip()
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
            logging.error(f"An error occurred while extracting data row: {e}")
            return pd.DataFrame()


class Financial_Instruments_Updater:
    def __init__(self):
        self.data_loader = DataLoader()

    def update_financial_instruments(self):
        """
        Function that updates the financial instruments dataset with a progress
        bar using pooling.
        """
        current_data = self.data_loader.load_financial_instruments()
        senators_data = self.data_loader.load_senators_trading()
        exclude_tickers = self.data_loader.load_exclude_tickers()

        if current_data.empty:
            current_data = pd.DataFrame(columns=['Ticker'])

        tickers = senators_data.Ticker.drop_duplicates()
        tickers = pd.concat([tickers, pd.Series(["^GSPC"])], ignore_index=True)
        tickers = fin_ticker_preparation(tickers, exclude_tickers)
        tickers = [ticker for ticker in tickers if not is_data_up_to_date(
            current_data, ticker
        )]
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(
            f"Processing {len(tickers)} tickers. Due to API requests "
            "limitations, this may take in tens of minutes. Please wait on "
            "this page..."
        )

        try:
            with Pool(processes=2) as pool:
                results = pool.map(self.process_ticker, [
                    (index, len(tickers), ticker, current_data, exclude_tickers)
                    for index, ticker in enumerate(tickers)
                ])
            if results:
                valid_results, excluded_ticker_results = zip(*results)
                valid_results = [
                    result for result in valid_results if result is not None and not result.empty and is_data_up_to_date(result, result['Ticker'].values[0])
                ]
                progress_bar.progress(100)
                excluded_ticker_dfs = [
                    ex for ex in excluded_ticker_results if ex is not None and not ex.empty
                ]
                if excluded_ticker_dfs:
                    new_excluded_tickers = pd.concat(
                        excluded_ticker_dfs, ignore_index=True
                    )
                    new_excluded_tickers = new_excluded_tickers.drop_duplicates(
                        subset=['Ticker']
                    )
                    new_excluded_tickers.to_csv(
                        os.path.join("Data", "exclude_tickers.csv"), index=False
                    )

                if valid_results:
                    update_data = pd.concat(valid_results, ignore_index=True)
                    current_data = pd.concat(
                        [current_data, update_data], ignore_index=True, join='outer'
                    )
                    current_data = current_data.drop_duplicates(subset=['Ticker'])
                    status_text.text(
                        f"All {len(update_data)} new records from the internet "
                        "loaded successfully and saved to financial_instruments.csv"
                    )
                    current_data.to_csv(
                        os.path.join("Data", "financial_instruments.csv"),
                        index=False
                    )
                else:
                    status_text.text(
                        f"All {len(valid_results)} new records from the internet "
                        "loaded successfully and saved to financial_instruments.csv"
                    )
            else:
                status_text.text("No new records were found.")
        except Exception as e:
            logging.error(f"An error occurred while updating financial instruments data, plaese repeat: {e}")

    def process_ticker(self, args):
        index, tickers, ticker, current_data, exclude_tickers = args
        print(f"Processing ticker: {ticker} - {index + 1}/{tickers}")
        if is_data_up_to_date(current_data, ticker):
            return pd.DataFrame(), pd.DataFrame()

        symbol_info = self.get_symbol_info(ticker)
        if symbol_info is None:
            exclude_tickers = add_to_exclude_tickers(ticker, exclude_tickers)
            return pd.DataFrame(), exclude_tickers

        history = self.get_symbol_history(ticker)
        if history is None:
            exclude_tickers = add_to_exclude_tickers(ticker, exclude_tickers)
            return pd.DataFrame(), exclude_tickers

        time.sleep(1.4)

        return pd.concat([symbol_info, history], axis=1), pd.DataFrame()

    def get_symbol_info(self, ticker):
        try:
            symbol = yf.Ticker(ticker)
            symbol_info = pd.json_normalize(symbol.info).dropna(how='all', axis=1)
            symbol_info.insert(0, 'Ticker', ticker)
            symbol_info = fin_info_preparation(symbol_info)

            if 'quoteType' not in symbol_info.columns and not symbol_info.iloc[:, -1].isna().all():
                return None

            return symbol_info

        except RequestException as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error for {ticker}: {e}")
            return None

    def get_symbol_history(self, ticker):
        try:
            symbol = yf.Ticker(ticker)
            history = symbol.history(period="max", interval="1mo").reset_index()

            if history.empty:
                return None

            return fin_history_preparation(history).set_index('Date').T.reset_index(drop=True)

        except RequestException as e:
            logging.error(f"Error fetching history for {ticker}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error for {ticker}: {e}")
            return None


class Senators_Information_Updater:
    def __init__(self):
        self.data_loader = DataLoader()

    def update_senators_information(self):
        """
        Function that updates the senators' information dataset with
        multiprocessing.
        """
        senators_data = self.data_loader.load_senators_trading()
        senators = senators_data.drop_duplicates(subset=['Politician'])[
            ['Politician', 'Chamber']
        ].reset_index(drop=True)
        senator_info_args = [
            (index, len(senators), row['Politician'], row['Chamber'])
            for index, row in senators.iterrows()
        ]
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(
            f"Processing senators information for {len(senators)} senators. "
            "Please wait..."
        )

        with Pool(os.cpu_count() // 2) as pool:
            results = pool.map(self.process_senator, senator_info_args)

        current_data = pd.concat(results, ignore_index=True)
        progress_bar.progress(100)
        status_text.text(f"All {len(results)} new records saved to senators_information.csv.")
        current_data.to_csv(os.path.join("Data", "senators_information.csv"), index=False)

        return None

    def process_senator(self, args):
        index, senators, politician, chamber = args
        print(f"Processing senator: {politician} - {index + 1}/{senators}")

        try:
            senator_page = wikipedia.page(f"{politician} (US {chamber} politician)")
            images = [img for img in senator_page.images if img.endswith(('png', 'jpg', 'svg'))]
            picture = get_profile_picture(images)

            return pd.DataFrame([{
                "Politician": politician,
                "Information": senator_page.summary,
                "Link": senator_page.url,
                "Picture": picture
            }])

        except wikipedia.exceptions.DisambiguationError:
            print(f"Non-process critical error for {politician}")
        except wikipedia.exceptions.PageError:
            print(f"Page not found for {politician}")
        except Exception as e:
            print(f"Unexpected error for {politician}: {e}")

        return None
