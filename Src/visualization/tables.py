"""
This script contains the functions that create the helpful tables that can be later displayed.
"""
import pandas as pd


# TODO tests, error handling, class
def top_five_purchased_stocks(data, politician, quoteType):
    """
    Create a table with the top 5 traded stocks and last transactions.
    """
    help_df = data[(data["Politician"] == politician) & (data["quoteType"] == quoteType) & (data["Transaction"] == "Purchase")]

    grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)

    if quoteType == "EQUITY":
        last_transaction = help_df.groupby(
            ["Ticker", "shortName", "sector"], as_index=False)["Traded"].max()

        # Merging the grouped data with last transaction
        top_five_with_last_transaction = (
            grouped_df
            .merge(last_transaction, how="left", on="Ticker")
            .rename(columns={
                "Invested": "Total Invested",
                "Traded": "Last Purchase",
                "shortName": "Name",
                "sector": "Sector"})
            .set_index("Ticker")
        )

        top_five_with_last_transaction = top_five_with_last_transaction[
            ["Name", "Sector", "Total Invested", "Last Purchase"]
        ]
        top_five_with_last_transaction = top_five_with_last_transaction.sort_values(
            by=["Total Invested", "Last Purchase"], ascending=[False, False]
        ).head(5)

        top_five_with_last_transaction["Total Invested"] = (
            top_five_with_last_transaction["Total Invested"]
            .apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
        )

    else:
        last_transaction = help_df.groupby(
            ["Ticker", "shortName"], as_index=False)["Traded"].max()

        # Merging the grouped data with last transaction
        top_five_with_last_transaction = (
            grouped_df
            .merge(last_transaction, how="left", on="Ticker")
            .rename(columns={
                "Invested": "Total Invested",
                "Traded": "Last Purchase",
                "shortName": "Name"})
            .set_index("Ticker")
        )

        top_five_with_last_transaction = top_five_with_last_transaction[
            ["Name", "Total Invested", "Last Purchase"]
        ]
        top_five_with_last_transaction = top_five_with_last_transaction.sort_values(
            by=["Total Invested", "Last Purchase"], ascending=[False, False]
        ).head(5)

        top_five_with_last_transaction["Total Invested"] = (
            top_five_with_last_transaction["Total Invested"]
            .apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
        )

    return top_five_with_last_transaction


# TODO tests, error handling, class
def top_five_sold_stocks(data, politician, quoteType):
    """
    Create a table with the top 5 sold stocks and last transactions.
    """
    help_df = data[(data["Politician"] == politician) & (data["quoteType"] == quoteType) & (data["Transaction"] == "Sale")]

    help_df["Invested"] = -help_df["Invested"]

    if quoteType == "EQUITY":
        grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)

        last_transaction = help_df.groupby(
            ["Ticker", "shortName", "sector"], as_index=False)["Traded"].last()

        top_five_with_last_transaction_sold = (
            grouped_df
            .merge(last_transaction, how="left", on="Ticker")
            .rename(columns={
                "Invested": "Total Sold",
                "Traded": "Last Purchase",
                "shortName": "Name",
                "sector": "Sector"})
            .set_index("Ticker")
        )

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold[
            ["Name", "Sector", "Total Sold", "Last Purchase"]
        ]
        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold.sort_values(
            by=["Total Sold", "Last Purchase"], ascending=[False, False]
        ).head(5)

        top_five_with_last_transaction_sold["Total Sold"] = (
            top_five_with_last_transaction_sold["Total Sold"]
            .apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
        )

    else:
        grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)

        last_transaction = help_df.groupby(
            ["Ticker", "shortName"], as_index=False)["Traded"].last()

        top_five_with_last_transaction_sold = (
            grouped_df
            .merge(last_transaction, how="left", on="Ticker")
            .rename(columns={
                "Invested": "Total Sold",
                "Traded": "Last Purchase",
                "shortName": "Name"})
            .set_index("Ticker")
        )

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold[
            ["Name", "Total Sold", "Last Purchase"]
        ]
        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold.sort_values(
            by=["Total Sold", "Last Purchase"], ascending=[False, False]
        ).head(5)

        top_five_with_last_transaction_sold["Total Sold"] = (
            top_five_with_last_transaction_sold["Total Sold"]
            .apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
        )

    return top_five_with_last_transaction_sold


def data_for_strategy_align_type(data):
    total_purchase_df = (
        data[data["Transaction"] == "Purchase"]
        .groupby(["Politician"], as_index=False)["Invested"]
        .sum()
        .rename(columns={"Invested": "Total Invested"})
    )

    total_purchase_type_df = (
        data[data["Transaction"] == "Purchase"]
        .groupby(["Politician", "quoteType"], as_index=False)["Invested"]
        .sum()
        .rename(columns={"Invested": "Total Invested Type"})
    )

    help_df_type = total_purchase_type_df.merge(total_purchase_df, how="left", on="Politician")

    help_df_type["Total Invested Type"] = (
        help_df_type["Total Invested Type"] * 100 / help_df_type["Total Invested"]
    )

    unique_politicians = pd.DataFrame({"Politician": help_df_type["Politician"].unique()})
    unique_type = pd.DataFrame({"quoteType": help_df_type["quoteType"].unique()})

    cross_joined_df = unique_politicians.merge(unique_type, how='cross')

    final_table = cross_joined_df.merge(help_df_type, how="left", on=["Politician", "quoteType"]).fillna(0)

    return final_table


def data_for_strategy_align_sector(data):
    total_purchase_type_df = (
        data[data["Transaction"] == "Purchase"]
        .groupby(["Politician", "quoteType"], as_index=False)["Invested"]
        .sum()
        .rename(columns={"Invested": "Total Invested"})
    )

    total_purchase_equity_df = total_purchase_type_df[total_purchase_type_df["quoteType"] == "EQUITY"]

    total_purchase_sector_df = (
        data[(data["Transaction"] == "Purchase") & (data["quoteType"] == "EQUITY")]
        .groupby(["Politician", "sector"], as_index=False)["Invested"]
        .sum()
        .rename(columns={"Invested": "Total Invested Sector"})
    )

    help_df_sector = total_purchase_sector_df.merge(total_purchase_equity_df, how="left", on="Politician")

    help_df_sector["Total Invested Sector"] = (
        help_df_sector["Total Invested Sector"] * 100 / help_df_sector["Total Invested"]
    )

    unique_politicians = pd.DataFrame({"Politician": help_df_sector["Politician"].unique()})
    unique_sector = pd.DataFrame({"sector": help_df_sector["sector"].unique()})

    cross_joined_df = unique_politicians.merge(unique_sector, how='cross')

    final_table = cross_joined_df.merge(help_df_sector, how="left", on=["Politician", "sector"]).fillna(0)

    return final_table
