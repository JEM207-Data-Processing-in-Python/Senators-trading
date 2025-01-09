import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from Src.scraping.scraper import DataLoader, SenatorsTradingUpdater


class TestDataLoader(unittest.TestCase):
    @patch("os.path.exists", return_value=False)
    @patch("builtins.print")
    @patch("pandas.read_csv")
    @patch("update_senators_trading")
    def test_load_data(self, mock_update, mock_read_csv, mock_print):
        data_loader = DataLoader()
        mock_read_csv.return_value = pd.DataFrame({"Ticker": ["AAPL", "GOOG"], "Amount": [100, 200]})
        result = data_loader.load_senators_trading()
        mock_update.assert_called_once()

        mock_print.assert_called_with("Error loading senators_trading.csv: senators_trading.csv not found.")
        self.assertEqual(result, pd.DataFrame())

        mock_read_csv.return_value = pd.DataFrame({"Ticker": ["AAPL", "GOOG"], "Amount": [100, 200]})
        result = data_loader.load_senators_trading()
        self.assertEqual(result.shape, (2, 2))
        self.assertTrue("Ticker" in result.columns)


class TestSenatorsTradingUpdater(unittest.TestCase):
    @patch("requests.post")
    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    @patch("senators_trading_updater.senators_data_preparation")
    def test_update_senators_trading(self, mock_senators_data_preparation, mock_to_csv, mock_read_csv, mock_post):
        # Setup mock data for loading
        mock_current_data = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOG'],
            'Politician': ['Senator 1', 'Senator 2'],
            'Transaction': ['Purchase', 'Sale'],
            'Amount': [100, 200],
            'Traded Date': ['2023-01-01', '2023-02-01'],
            'Filed Date': ['2023-01-02', '2023-02-02']
        })
        mock_read_csv.return_value = mock_current_data

        # Setup mock response for requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "table": '<table><tr class="data-table__row"><td data-title="Stock">MSFT</td></tr></table>',
            "total_pages": 2
        }
        mock_post.return_value = mock_response

        # Setup mock for senators data preparation
        mock_senator_data = pd.DataFrame({
            'Ticker': ['MSFT'],
            'Politician': ['Senator 3'],
            'Transaction': ['Purchase'],
            'Amount': [150],
            'Traded Date': ['2023-03-01'],
            'Filed Date': ['2023-03-02']
        })
        mock_senators_data_preparation.return_value = mock_senator_data

        # Run the method
        updater = SenatorsTradingUpdater()
        updater.update_senators_trading()

        # Assert the post request was called
        mock_post.assert_called_with(
            'https://trendspider.com/markets/wp-admin/admin-ajax.php',
            data={'action': 'get_congresstrading_table', 'page': 1, 'limit': 10000, 'politician': '', 'ticker': ''},
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        # Assert that the correct data is appended
        mock_to_csv.assert_called_once_with("Data/senators_trading.csv", index=False)

        # Check that new data was correctly appended
        new_data = pd.DataFrame({
            'Ticker': ['MSFT'],
            'Politician': ['Senator 3'],
            'Transaction': ['Purchase'],
            'Amount': [150],
            'Traded Date': ['2023-03-01'],
            'Filed Date': ['2023-03-02']
        })

        # Verifying the new data is added to the file
        args, kwargs = mock_to_csv.call_args
        df_saved = args[0]
        pd.testing.assert_frame_equal(df_saved, pd.concat([mock_current_data, new_data], ignore_index=True))
