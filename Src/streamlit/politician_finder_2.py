"""
This file contains the helper code for the Streamlit app's Politician Finder.
"""
import pandas as pd


def most_trade_type_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most frequent trade type (quoteType) the selected politician
    invests in, based on the "Purchase" transactions in the dataset.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating which trade type the politician invests the
    most in.

    Note:
    - Returns a message about purchases if they exist; otherwise, indicates no
    purchases.
    """
    try:
        most_trade_type_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
        ]
            .groupby("quoteType", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["quoteType"]
        )

        message_1 = (
            f"{selected_politician} invests the most often into "
            f"{most_trade_type_politician}"
        )
    except Exception:
        message_1 = (f"{selected_politician} has not performed any purchases "
                     "during documented time period.")

    return message_1


def most_traded_volume_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the total volume of the most traded instrument (quoteType) by
    the selected politician, based on "Purchase" transactions.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the total average amount purchased by the
    politician.

    Note:
    - Returns the amount purchased for the most traded instrument or an empty
    string if no data is available.
    """
    try:
        most_traded_volume_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")
        ]
            .groupby("quoteType", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["Invested"]
        )
        most_traded_volume_politician = f"{most_traded_volume_politician:,.0f}"

        message_2 = (
            f"with the total average amount purchased of "
            f"{most_traded_volume_politician} USD."
        )
    except Exception:
        message_2 = ""

    return message_2


def most_traded_sector_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most traded sector and its total volume for equity
    investments (quoteType == 'EQUITY') by the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the most traded sector for equity investments
    and its total volume.

    Note:
    - Returns a message about equity investments in a sector if available;
    otherwise, indicates no data.
    """
    try:
        most_traded_sector_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["sectorKey"]
        )
    except Exception:
        most_traded_sector_politician = "Empty"

    try:
        most_traded_sector_volume = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[0]["Invested"]
        )
        most_traded_sector_volume = f"{most_traded_sector_volume:,.0f}"

    except Exception:
        most_traded_sector_volume = "Empty"

    if most_traded_sector_politician == "Empty":
        message_3 = "They have not invested in EQUITY either."
    else:
        message_3 = (
            f"When it comes to EQUITY, this politician mostly invests in "
            f"{most_traded_sector_politician} with the total average volume "
            f"invested of {most_traded_sector_volume} USD."
        )

    return message_3


def most_sold_sector_politician(data: pd.DataFrame, selected_politician: str) -> str:
    """
    Identifies the most sold sector and its total volume for equity sales
    (quoteType == 'EQUITY') by the selected politician.

    Parameters:
    - data (pd.DataFrame): The dataset containing transaction information.
    - selected_politician (str): The name of the politician.

    Returns:
    - str: A message indicating the most sold sector for equity sales and its
    total volume.

    Note:
    - Returns a message about equity sales in a sector if available; otherwise,
    indicates no data.
    """
    try:
        most_sold_sector_politician = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Sale") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[-1]["sectorKey"]
        )
    except Exception:
        most_sold_sector_politician = "Empty"

    try:
        most_sold_sector_volume = (data[
            (data["Politician"] == selected_politician) & (data["Transaction"] == "Sale") & (data["quoteType"] == "EQUITY")
        ]
            .groupby("sectorKey", as_index=False)["Invested"]
            .sum()
            .sort_values(by="Invested", ascending=False)
            .iloc[-1]["Invested"]
        )

        most_sold_sector_volume = f"{-most_sold_sector_volume:,.0f}"
    except Exception:
        most_sold_sector_volume = "Empty"

    if most_sold_sector_politician == "Empty":
        message_4 = (
            "They did not perform any sales of EQUITY during the documented "
            "time period."
        )
    else:
        message_4 = (
            f"{selected_politician} sold EQUITY mostly in "
            f"{most_sold_sector_politician} sector with the total average "
            f"volume sold of {most_sold_sector_volume} USD."
        )

    return message_4
