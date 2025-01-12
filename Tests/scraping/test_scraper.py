"""
This is a test file for the scraper.py file.
"""

import unittest
from unittest.mock import patch, Mock
import pandas as pd
from bs4 import BeautifulSoup
import wikipedia

from Src.scraping.scraper import (
    DataLoader,
    Senators_Trading_Updater,
    Financial_Instruments_Updater,
    Senators_Information_Updater
)


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoader()

    @patch('pandas.read_csv')
    def test_load_senators_trading(self, mock_read_csv):
        mock_df = pd.DataFrame({'Ticker': ['AAPL', 'GOOGL']})
        mock_read_csv.return_value = mock_df

        # Test function
        result = self.data_loader.load_senators_trading()
        pd.testing.assert_frame_equal(result, mock_df)
        mock_read_csv.assert_called_once()

    @patch('pandas.read_csv')
    def test_load_financial_instruments(self, mock_read_csv):
        mock_df = pd.DataFrame({'Ticker': ['AAPL', 'GOOGL']})
        mock_read_csv.return_value = mock_df
        result = self.data_loader.load_financial_instruments()
        pd.testing.assert_frame_equal(result, mock_df)


class TestSenatorsTrading(unittest.TestCase):
    def setUp(self):
        self.updater = Senators_Trading_Updater()

    @patch('requests.post')
    def test_fetch_data(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'table': '<table></table>', 'total_pages': 2}
        mock_post.return_value = mock_response

        # Test function
        result = self.updater.fetch_data(1)
        self.assertEqual(result.status_code, 200)
        mock_post.assert_called_once()

    def test_extract_row_data(self):
        html = '''
        <tr class="data-table__row">
            <td data-title="Stock">AAPL</td>
            <td data-title="Politician"><a>John Doe</a><abbr>D</abbr><div><small>Senate</small></div></td>
            <td data-title="Transaction"><span>Buy</span><div><small>$15,000 - $50,000</small></div></td>
            <td data-title="Traded"><div>Jan 01, 2023</div></td>
            <td data-title="Filed"><div>Feb 01, 2023</div></td>
        </tr>
        '''
        row = BeautifulSoup(html, 'html.parser').find('tr')
        exclude_tickers = pd.DataFrame({'Ticker': []})

        # Test function
        result = self.updater.extract_row_data(row, exclude_tickers)
        self.assertEqual(result['Ticker'].iloc[0], 'AAPL')
        self.assertEqual(result['Politician'].iloc[0], 'John Doe')


class TestFinancialInstruments(unittest.TestCase):
    def setUp(self):
        self.updater = Financial_Instruments_Updater()

    @patch('yfinance.Ticker')
    def test_get_symbol_history(self, mock_ticker):
        mock_history = pd.DataFrame({
            'Open': [100],
            'High': [110],
            'Low': [90],
            'Close': [105],
            'Volume': [1000000],
            'Date': [pd.Timestamp('2023-01-01')]
        })
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_history
        mock_ticker.return_value = mock_ticker_instance

        # Test function
        result = self.updater.get_symbol_history('AAPL')
        self.assertTrue(isinstance(result, pd.DataFrame))


class TestSenatorsInformation(unittest.TestCase):
    def setUp(self):
        self.updater = Senators_Information_Updater()

    @patch('wikipedia.page')
    def test_process_senator(self, mock_wiki_page):
        mock_page = Mock()
        mock_page.summary = "Test summary"
        mock_page.url = "http://test.com"
        mock_page.images = ["test.jpg"]
        mock_wiki_page.return_value = mock_page

        # Test function
        result = self.updater.process_senator((0, 1, "John Doe", "Senate"))
        self.assertIsNotNone(result)
        self.assertEqual(result['Politician'].iloc[0], "John Doe")
        self.assertEqual(result['Information'].iloc[0], "Test summary")

    @patch('wikipedia.page')
    def test_process_senator_error_handling(self, mock_wiki_page):
        mock_wiki_page.side_effect = wikipedia.exceptions.PageError("Test")

        # Test function
        result = self.updater.process_senator((0, 1, "Nonexistent Senator", "Senate"))
        self.assertIsNone(result)
