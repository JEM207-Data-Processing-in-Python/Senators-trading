"""
This is a test file for the instrument_finder.py file
"""
import unittest
import pandas as pd

from Src.streamlit.instrument_finder import instrument_information


class TestInstrumentInformation(unittest.TestCase):

    def setUp(self):
        """Set up a mock dataset for testing."""
        data = {
            'Name': ['Apple Inc.', 'Tesla Inc.', 'Unknown Corp'],
            'Ticker': ['AAPL', 'TSLA', 'Unknown'],
            'city': ['Cupertino', 'Palo Alto', 'Unknown'],
            'country': ['USA', 'USA', 'Unknown'],
            'industryKey': ['Technology', 'Automotive', 'Unknown'],
            'sectorKey': ['Tech', 'Auto', 'Unknown'],
            'longBusinessSummary': ['Designs and manufactures electronics', 'Electric vehicle manufacturer', 'Unknown'],
            'currency': ['USD', 'USD', 'Unknown'],
            'quoteType': ['Equity', 'Equity', 'Unknown'],
            'shortName': ['Apple', 'Tesla', 'Unknown'],
            'longName': ['Apple Inc.', 'Tesla, Inc.', 'Unknown'],
            'financialCurrency': ['USD', 'USD', 'Unknown']
        }
        self.df = pd.DataFrame(data)

    def test_valid_instrument(self):
        """Test when valid instrument data is available."""
        selected_instrument = 'Apple Inc.'
        expected_output = (
            "The Financial instrument ticker is **AAPL**. It is a **Equity** fiancial instrument. "
            "It is known as **Apple**. The full name of the company is **Apple Inc.** "
            "The company is located in **Cupertino**, **USA**. The company operates in the **Tech** sector. "
            "The company's industry is **Technology**. The company's currency is **USD**. "
            "\n\nThe company is involved in Designs and manufactures electronics."
        )
        result = instrument_information(self.df, selected_instrument)
        self.assertEqual(result, expected_output)

    def test_instrument_with_unknown_data(self):
        """Test when some values are 'Unknown'."""
        selected_instrument = 'Tesla Inc.'
        expected_output = (
            "The Financial instrument ticker is **TSLA**. It is a **Equity** fiancial instrument. "
            "It is known as **Tesla**. The full name of the company is **Tesla, Inc.** "
            "The company is located in **Palo Alto**, **USA**. The company operates in the **Auto** sector. "
            "The company's industry is **Automotive**. The company's currency is **USD**. "
            "\n\nThe company is involved in Electric vehicle manufacturer."
        )
        result = instrument_information(self.df, selected_instrument)
        self.assertEqual(result, expected_output)

    def test_all_unknown_values(self):
        """Test when all values for the instrument are 'Unknown'."""
        selected_instrument = 'Unknown Corp'
        expected_output = "        "
        result = instrument_information(self.df, selected_instrument)
        self.assertEqual(result, expected_output)
