"""
This script contains the functions that create the helpfull tables that can be later displayed.
"""

def top_five_purchased_stocks(data, politician, quoteType):
    """
    Create a table with the top 5 traded stocks and last transactions.
    """
    help_df = data[(data["Politician"] == politician) &
                    (data["quoteType"] == quoteType) &
                    (data["Transaction"] == "Purchase")]
    
    grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)
    
    if quoteType == "EQUITY":
        last_transaction = help_df.groupby(["Ticker", "shortName", "sector"], as_index=False)["Traded"].max()
        
        # Merging the grouped data with last transaction
        top_five_with_last_transaction = (grouped_df
                                          .merge(last_transaction, how="left", on="Ticker")
                                          .rename(columns={"Invested": "Total Invested", "Traded": "Last Purchase", "shortName": "Name", "sector": "Sector"})
                                          .set_index("Ticker"))

        top_five_with_last_transaction = top_five_with_last_transaction[["Name", "Sector", "Total Invested", "Last Purchase"]]   

        top_five_with_last_transaction = top_five_with_last_transaction.sort_values(by=["Total Invested", "Last Purchase"], ascending=[False, False]).head(5)

        top_five_with_last_transaction["Total Invested"] = top_five_with_last_transaction["Total Invested"].apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
    
    else:
        last_transaction = help_df.groupby(["Ticker", "shortName"], as_index=False)["Traded"].max()
        
        # Merging the grouped data with last transaction
        top_five_with_last_transaction = (grouped_df
                                          .merge(last_transaction, how="left", on="Ticker")
                                          .rename(columns={"Invested": "Total Invested", "Traded": "Last Purchase", "shortName": "Name"})
                                          .set_index("Ticker"))

        top_five_with_last_transaction = top_five_with_last_transaction[["Name", "Total Invested", "Last Purchase"]]   

        top_five_with_last_transaction = top_five_with_last_transaction.sort_values(by=["Total Invested", "Last Purchase"], ascending=[False, False]).head(5)

        # Replace NaN values with "Unknown" or "N/A"
        top_five_with_last_transaction["Name"] = top_five_with_last_transaction["Name"].fillna("Unknown")
        top_five_with_last_transaction["Last Purchase"] = top_five_with_last_transaction["Last Purchase"].fillna("N/A")

        top_five_with_last_transaction["Total Invested"] = top_five_with_last_transaction["Total Invested"].apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")

    return top_five_with_last_transaction


def top_five_sold_stocks(data, politician, quoteType):
    """
    Create a table with the top 5 sold stocks and last transactions.
    """
    help_df = data[(data["Politician"] == politician) &
                    (data["quoteType"] == quoteType) &
                    (data["Transaction"] == "Sale")]
    
    help_df["Invested"] = -help_df["Invested"]

    if quoteType == "EQUITY":
        grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)

        last_transaction = help_df.groupby(["Ticker", "shortName", "sector"], as_index=False)["Traded"].last()

        top_five_with_last_transaction_sold = (grouped_df
                                      .merge(last_transaction, how = "left", on = "Ticker")
                                      .rename(columns = {"Invested" : "Total Sold", "Traded" : "Last Purchase", "shortName":"Name", "sector":"Sector"})
                                      .set_index("Ticker"))

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold[["Name", "Sector", "Total Sold", "Last Purchase"]]   

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold.sort_values(by = ["Total Sold", "Last Purchase"], ascending = [False, False]).head(5)

        top_five_with_last_transaction_sold["Total Sold"] = top_five_with_last_transaction_sold["Total Sold"].apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
    
    else:
        grouped_df = help_df.groupby("Ticker", as_index=False)["Invested"].sum().round(0)

        last_transaction = help_df.groupby(["Ticker", "shortName"], as_index=False)["Traded"].last()

        top_five_with_last_transaction_sold = (grouped_df
                                      .merge(last_transaction, how = "left", on = "Ticker")
                                      .rename(columns = {"Invested" : "Total Sold", "Traded" : "Last Purchase", "shortName":"Name"})
                                      .set_index("Ticker"))

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold[["Name", "Total Sold", "Last Purchase"]]   

        top_five_with_last_transaction_sold = top_five_with_last_transaction_sold.sort_values(by = ["Total Sold", "Last Purchase"], ascending = [False, False]).head(5)

        top_five_with_last_transaction_sold["Total Sold"] = top_five_with_last_transaction_sold["Total Sold"].apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")
    return top_five_with_last_transaction_sold