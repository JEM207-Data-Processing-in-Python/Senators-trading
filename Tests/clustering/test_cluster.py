"""
This file contains the test functions for the cluster.py module.
"""
import pytest
import pandas as pd

from Src.clustering.cluster import best_alignment


# Test Data
data_general = pd.DataFrame({
    "Politician": ["A", "B", "C"],
    "Total Invested Type": [100, 200, 300],
    "Total Invested Sector": [150, 250, 350]
})

data_user = pd.DataFrame({
    "Politician": ["A", "B", "C"],
    "Invested by User": [110, 200, 280]
})


def test_best_alignment_invalid_join_column():
    """
    Test the function when the join column doesn't exist in one of the DataFrames.
    """
    with pytest.raises(KeyError):
        best_alignment(data_general, data_user, join="NonExistentColumn")
