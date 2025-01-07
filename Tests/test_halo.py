
from Src.dummy.helo import add  # Import the dummy function


def test_add():
    """
    Test the add function with some basic test cases.
    """
    # Test with positive numbers
    assert add(1, 2) == 3

    # Test with negative numbers
    assert add(-1, -2) == -3

    # Test with zero
    assert add(0, 0) == 0

    # Test with mixed positive and negative numbers
    assert add(10, -5) == 5
