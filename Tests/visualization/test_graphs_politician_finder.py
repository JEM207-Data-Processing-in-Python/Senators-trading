"""
This file contains the tests for the graphs_politician_finder.py file.
"""
import pytest
import pandas as pd
from unittest.mock import patch
import plotly.graph_objects as go

from Src.visualization.graphs_politician_finder import Politician_Data_Visualizer


@pytest.fixture
def sample_data():
    data = {
        'Politician': ['Politician A', 'Politician A', 'Politician B', 'Politician B'],
        'Traded': ['2025-01-01', '2025-01-02', '2025-01-01', '2025-01-02'],
        'Invested': [1000, 2000, 1500, 2500],
        'Transaction': ['Purchase', 'Purchase', 'Sale', 'Sale'],
        'Sector': ['Tech', 'Health', 'Tech', 'Finance'],
        'Instrument': ['Stock', 'Bond', 'Stock', 'Bond'],
        'Party': ['Party A', 'Party A', 'Party B', 'Party B']  # Added the 'Party' column
    }
    df = pd.DataFrame(data)
    df['Traded'] = pd.to_datetime(df['Traded'])
    return df


def test_grouping_for_barchart(sample_data):
    visualizer = Politician_Data_Visualizer(sample_data)

    # Test function
    figure = visualizer.grouping_for_barchart('Politician', 'Politician A')
    assert isinstance(figure, go.Figure)
    assert figure.layout.title.text == "Total Investment per Month of Politician A"


def test_pie_chart_advanced(sample_data):
    visualizer = Politician_Data_Visualizer(sample_data)

    # Test function
    figure = visualizer.pie_chart_advanced('Purchase', 'Sector', 'Politician A')
    assert isinstance(figure, go.Figure)
    assert figure.layout.title.text == "Average Investment of \n Politician A by Sector - Purchase"


@patch('Src.streamlit.politician_finder.five_days')
def test_five_days_graph(mock_five_days, sample_data):
    mock_five_days.return_value = pd.DataFrame({
        'Traded': ['2025-01-01', '2025-01-02'],
        'Invested': [5000, 4000]
    })
    visualizer = Politician_Data_Visualizer(sample_data)

    # Test function
    figure = visualizer.five_days_graph('Politician A')
    assert isinstance(figure, go.Figure)
    assert figure.layout.title.text == "Days with the biggest trading volume of Politician A"
