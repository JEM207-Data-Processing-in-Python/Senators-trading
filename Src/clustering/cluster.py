"""
This module contains the functions to cluster the data and recommend the best alignment
"""
import pandas as pd


def best_alignment(data_general: pd.DataFrame, data_user: pd.DataFrame, join: str) -> pd.DataFrame:
    """
    This function calculates the alignment between general data (e.g., Total Invested Type)
    and user-provided data (e.g., Invested by User) based on a common column.
    It computes a Mean Squared Error (MSE) score and alignment percentage for each politician,
    ranks the top 5 politicians based on the best alignment, and returns the resulting DataFrame.

    Args:
        data_general (pd.DataFrame): The general data DataFrame, which includes columns such as 'Total Invested Type'.
        data_user (pd.DataFrame): The user data DataFrame, which includes columns such as 'Invested by User'.
        join (str): The column name used to join both DataFrames (e.g., 'Politician').

    Returns:
        pd.DataFrame: A DataFrame containing the top 5 politicians based on the best alignment score, with columns:
            - Politician (str): Name of the politician.
            - Alignment (%) (float): The alignment score as a percentage.
    """
    # Merge data frames on 'type'
    help_df = data_general.merge(data_user, how="left", on=join)

    # Calculate the squared difference as a "score" (penalizing larger differences)
    help_df["score"] = (help_df["Total Invested"] - help_df["Invested by User"]) ** 2

    # Calculate alignment score based on the normalized difference, clip to avoid negatives
    help_df["alignment"] = (1 - abs(help_df["Total Invested"] - help_df["Invested by User"]) / help_df["Total Invested"].replace(0, 1)).clip(lower=0)

    # Group by Politician and calculate the average score and alignment
    grouped_df_type = help_df.groupby("Politician", as_index=False)["score"].mean()
    grouped_df_alignment = help_df.groupby("Politician", as_index=False)["alignment"].mean()
    grouped_df_alignment["alignment"] = grouped_df_alignment["alignment"] * 100

    # Merge the grouped data frames and output
    top_5_politicians = (
        grouped_df_type
        .merge(grouped_df_alignment, how="left", on="Politician")
        .sort_values(by=["alignment", "score"], ascending=[False, True])
        .rename(columns={"score": "MSE score", "alignment": "Alignment (%)"})
        .reset_index(drop=True)
        .head(5)
    )
    top_5_politicians = top_5_politicians.drop(columns=["MSE score"])
    top_5_politicians.index = top_5_politicians.index + 1

    return top_5_politicians
