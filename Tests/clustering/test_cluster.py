"""
This file contains the test functions for the cluster.py module.
"""
import pytest
import pandas as pd
from Src.clustering.cluster import best_alignment


@pytest.fixture
def sample_data():
    # Sample data
    data_general = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Total Invested': [1000, 1500, 2000, 2500, 3000]
    })
    data_user = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Invested by User': [900, 1550, 1950, 2450, 3100]
    })

    return data_general, data_user


def test_best_alignment_basic(sample_data):
    data_general, data_user = sample_data

    # Test function
    result = best_alignment(data_general, data_user, 'Politician')
    assert len(result) == 5
    assert set(result.columns) == {'Politician', 'Alignment (%)'}
    for alignment in result['Alignment (%)']:
        assert 0 <= alignment <= 100


def test_best_alignment_perfect_match():
    data_general = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Total Invested': [1000, 1500, 2000, 2500, 3000]
    })
    data_user = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Invested by User': [1000, 1500, 2000, 2500, 3000]
    })

    # Test function
    result = best_alignment(data_general, data_user, 'Politician')
    for alignment in result['Alignment (%)']:
        assert alignment == 100


def test_best_alignment_empty_data():
    data_general = pd.DataFrame(columns=['Politician', 'Total Invested'])
    data_user = pd.DataFrame(columns=['Politician', 'Invested by User'])

    # Test function
    result = best_alignment(data_general, data_user, 'Politician')
    assert result.empty


def test_best_alignment_no_alignment():
    data_general = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Total Invested': [1000, 1500, 2000, 2500, 3000]
    })
    data_user = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Invested by User': [5000, 6000, 7000, 8000, 9000]
    })

    # Test function
    result = best_alignment(data_general, data_user, 'Politician')
    for alignment in result['Alignment (%)']:
        assert alignment == 0 or alignment < 1


def test_best_alignment_order():
    data_general = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Total Invested': [1000, 1500, 2000, 2500, 3000]
    })
    data_user = pd.DataFrame({
        'Politician': ['A', 'B', 'C', 'D', 'E'],
        'Invested by User': [800, 1550, 1950, 2450, 3100]
    })

    # Test function
    result = best_alignment(data_general, data_user, 'Politician')
    assert result['Alignment (%)'].is_monotonic_decreasing
