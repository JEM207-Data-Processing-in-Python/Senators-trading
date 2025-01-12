"""
This file contains the Tests for the graphs in Instrument Finder page.
"""
import unittest
import pandas as pd
from datetime import datetime
from plotly.graph_objects import Figure
from Src.visualization.graphs_istrument_finder import PoliticianGraph


class TestPoliticianGraph(unittest.TestCase):
    def setUp(self):
        data = {
            'Traded': [datetime(2022, 1, 1), datetime(2022, 2, 1)],
            'Invested': [10000, 15000],
            'Gain': [5, 10],
            'Profit': [500, 1500],
            'S&P 500': [3, 7],
            'Ticker': ['AAPL', 'MSFT'],
            'Name': ['AAPL - Apple Inc.', 'MSFT - Microsoft Corp.'],
            'Politician': ['Politician A', 'Politician A'],
            '2022-01-01': [150, 155],
            '2022-02-01': [160, 165]
        }
        self.politician_data = pd.DataFrame(data)
        self.selected_instrument = 'AAPL - Apple Inc.'
        self.graph = PoliticianGraph(self.politician_data, self.selected_instrument)

    def test_generate_graph(self):
        # Test function
        fig = self.graph.generate_graph()
        self.assertIsInstance(fig, Figure)
        self.assertGreater(len(fig.data), 0, "No data traces found in the figure.")
        self.assertEqual(fig.data[0].name, 'Price', "The trace name is not 'Price'.")

        for traded_date in self.politician_data['Traded']:
            # Test function
            vline_x_values = [str(shape['x0'].date()) for shape in fig.layout.shapes if shape['type'] == 'line']
            self.assertIn(traded_date.strftime('%Y-%m-%d'), vline_x_values, f"Vertical line for traded date {traded_date} not found.")

    def test_graph_layout(self):
        # Test function
        fig = self.graph.generate_graph()

        self.assertEqual(fig.layout.title.text, f"{self.selected_instrument} - Price graph")
        self.assertEqual(fig.layout.xaxis.title.text, "Date")
        self.assertEqual(fig.layout.yaxis.title.text, "Price")
