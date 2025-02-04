"""
This file contains the tests for the graphs_utils.py file.
"""
import pytest
import pandas as pd

from Src.visualization.graphs_utils import get_the_color


def test_get_the_color():
    data = pd.DataFrame({
        "Politician": ["Alice", "Bob", "Charlie"],
        "Party": ["R", "D", "I"]
    })

    # Test function
    assert get_the_color("Alice", data) == "red"
    assert get_the_color("Bob", data) == "blue"
    assert get_the_color("Charlie", data) == "white"
    with pytest.raises(IndexError):
        get_the_color("David", data)
