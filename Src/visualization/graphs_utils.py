"""
This file contains the utility functions used in the visualization of the data.
"""
import pandas as pd


def get_the_color(politician: str, data: pd.DataFrame) -> str:
    """
    Determines the color associated with the political party of a given politician.

    :param politician: str - The name of the politician whose party color is to be determined.
    :param data: pd.DataFrame - A pandas DataFrame containing columns "Politician" and "Party" - ("R" or "D").
    
    :return: str - The color associated with the politician's party. Returns "red" for Republican, "blue" for Democrat.
    """
    try:
        party = data[data["Politician"] == politician].iloc[0]["Party"]
        if party == "R":
            color = "red"
        elif party == "D":
            color = "blue"
    except Exception:
        print(f"Politician {politician} not found in the dataset", "error in get_the_color(politician, data) in graphs utilities")

    return color