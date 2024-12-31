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

    grouped_df["Invested"] = grouped_df["Invested"].apply(lambda x: f"{int(x):,}".replace(",", " ") + " USD")

    last_transaction = help_df.groupby(["Ticker", "shortName"], as_index=False)["Traded"].last()

    top_five = grouped_df.sort_values(by = "Invested", ascending = False).head(5)

    top_five_with_last_transaction = (top_five
                                      .merge(last_transaction, how = "left", on = "Ticker")
                                      .rename(columns = {"Invested" : "Total Invested", "Traded" : "Last Purchase", "shortName":"Name"})
                                      .set_index("Ticker"))

    top_five_with_last_transaction = top_five_with_last_transaction[["Name", "Total Invested", "Last Purchase"]]   
    
    return top_five_with_last_transaction