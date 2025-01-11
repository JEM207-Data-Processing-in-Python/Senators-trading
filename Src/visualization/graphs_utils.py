"""
This file contains the utility functions used in the visualization of the data.
"""
import pandas as pd
import seaborn as sns


def get_the_color(politician: str, data: pd.DataFrame) -> str:
    """
    Determines the color associated with the political party of a given politician.

    :param politician: str - The name of the politician whose party color is to be determined.
    :param data: pd.DataFrame - A pandas DataFrame containing columns "Politician" and "Party" - ("R" or "D").

    :return: str - The color associated with the politician's party. Returns "red" for Republican, "blue" for Democrat, and "white" for Independent.
    """
    party = data[data["Politician"] == politician].iloc[0]["Party"]
    if party == "R":
        color = "red"
    elif party == "D":
        color = "blue"
    elif party == "I":
        color = "white"

    return color


def same_color_across_pie_charts(unique_elements: list) -> dict:
    """
    Generates a color mapping for a list of unique elements based on a color palette.

    :param unique_elements: list - A list of unique elements for which color mapping needs to be created (e.g., politicians or categories).
    
    :return: dict - A dictionary where each key is an element from `unique_elements`, and the corresponding value is a color in hexadecimal format.
    """
    color_palette = sns.color_palette("tab10", len(unique_elements)).as_hex()

    color_mapping = dict(zip(unique_elements, color_palette))

    return color_mapping
