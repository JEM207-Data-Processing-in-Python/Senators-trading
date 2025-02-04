"""
This file contains the tests for the graphs_align_investment.py file.
"""
import pandas as pd
from plotly.graph_objects import Figure

from Src.visualization.graphs_align_investment import Pie_Chart_Align_Investment

sample_data = pd.DataFrame({
    "Politician": ["Politician1", "Politician1", "Politician2", "Politician2"],
    "Sector": ["Tech", "Finance", "Tech", "Finance"],
    "Invested": [100, 200, 150, 250],
    "Transaction": ["Purchase", "Purchase", "Purchase", "Sale"]
})
user_data = pd.DataFrame({
    "Sector": ["Tech", "Finance", "Energy"],
    "Invested by User": [100, 150, 200]
})


def test_same_color_across_pie_charts():
    sectors = ["Tech", "Finance", "Energy"]
    pie_chart = Pie_Chart_Align_Investment(sectors)

    # Test function
    colors = pie_chart.colors
    assert len(colors) == len(sectors), "Number of colors should match the number of sectors"
    assert all(isinstance(color, str) and color.startswith("#") for color in colors.values()), "Colors should be in hex format"


def test_create_politician_chart():
    pie_chart = Pie_Chart_Align_Investment(["Tech", "Finance", "Energy"])

    # Test function
    fig = pie_chart.create_politician_chart(sample_data, purchase="Purchase", subset="Sector", politician="Politician1")
    assert isinstance(fig, Figure), "Output should be a Plotly Figure object"
    assert "Politician1" in fig.layout.title.text, "Title should contain the politician's name"


def test_create_user_chart():
    pie_chart = Pie_Chart_Align_Investment(["Tech", "Finance", "Energy"])

    # Test function
    fig = pie_chart.create_user_chart(user_data, what="Sector")
    assert isinstance(fig, Figure), "Output should be a Plotly Figure object"
    assert fig.layout.title.text == "Your exposure to the EQUITY:", "Title should be 'Your exposure to the EQUITY:'"
    labels = [label for label in fig.data[0].labels]
    assert all(label in user_data["Sector"].values for label in labels), "Labels should match the data's 'Sector' column"
