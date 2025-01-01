"""
This script contains the functions that create the text and tables for the first page of the Streamlit app.
"""
import streamlit as st
import pandas as pd
from src.visualization.tables import top_five_purchased_stocks
from src.visualization.tables import top_five_sold_stocks


# TODO: tests, error handling
def party_politician(data, selected_politician):
    #Get information for interactive text
    party_politician = data[data["Politician"] == selected_politician]["Party"].unique()
    if party_politician == "R":
        party_politician = "Republican Party"
    elif party_politician == "D":
        party_politician = "Democratic Party"
    else:
        party_politician = "Third Party"
    
    return party_politician


# TODO: tests, error handling
def chmaber_politician(data, selected_politician):
    chamber_politician = data[data["Politician"] == selected_politician]["Chamber"].unique()
    if chamber_politician == "House":
        chamber_politician = "House of Representatives"
    elif chamber_politician == "Senate":
        chamber_politician = "Senate"
    else:
        chamber_politician = "Unknown Chamber" 

    return chamber_politician


# TODO: tests, error handling
def first_trade_politician(data, selected_politician):
    first_trade_politician = data[data["Politician"] == selected_politician]["Traded"].min()

    return first_trade_politician


# TODO: tests, error handling
def last_trade_politician(data, selected_politician):
    last_trade_politician = data[data["Politician"] == selected_politician]["Traded"].max()

    return last_trade_politician


# TODO: tests, error handling
def total_invested_politician(data, selected_politician):
    total_invested_politician = data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")]["Invested"].sum()

    total_invested_politician = f"{total_invested_politician:,.0f}"

    return total_invested_politician


# TODO: tests, error handling
def total_sold_politician(data, selected_politician):
    help_df = data.copy()

    help_df["Invested"] = -help_df["Invested"]

    total_sold_politician = help_df[(help_df["Politician"] == selected_politician) & (help_df["Transaction"] == "Sale")]["Invested"].sum()  

    total_sold_politician = f"{total_sold_politician:,.0f}"
    
    return total_sold_politician


# TODO: tests, error handling
def most_trade_type_politician(data, selected_politician):
    try:
        most_trade_type_politician = (data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")]
                                  .groupby("quoteType", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[0]["quoteType"])

        message_1 = (f"{selected_politician} invests the most often into {most_trade_type_politician}")
    except:
        message_1 = (f"{selected_politician} has not performed any purchases during documented time period.")

    return message_1


# TODO: tests, error handling
def most_traded_volume_politician(data, selected_politician):
    try:
        most_traded_volume_politician = (data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")]
                                  .groupby("quoteType", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[0]["Invested"])
        most_traded_volume_politician = f"{most_traded_volume_politician:,.0f}"

        message_2 = (f"with the total average amount purchased of {most_traded_volume_politician} USD.")
    except:
        message_2 = ""

    return message_2


# TODO: tests, error handling
def most_traded_sector_politician(data, selected_politician):
    try:
        most_traded_sector_politician = (data[(data["Politician"] == selected_politician) &
                                           (data["Transaction"] == "Purchase") &
                                           (data["quoteType"] == "EQUITY")]
                                  .groupby("sector", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[0]["sector"])
    except:
        most_traded_sector_politician = "Empty"

    
    try:
        most_traded_sector_volume = (data[(data["Politician"] == selected_politician) &
                                           (data["Transaction"] == "Purchase") &
                                           (data["quoteType"] == "EQUITY")]
                                  .groupby("sector", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[0]["Invested"])
        most_traded_sector_volume = f"{most_traded_sector_volume:,.0f}"

    except:
        most_traded_sector_volume = "Empty"

    if most_traded_sector_politician == "Empty":
        message_3 = ("They has not invested in EQUITY either.")
    else:
        message_3 = (f"When it comes to EQUITY, this politician mostly invest in {most_traded_sector_politician} \
            with the total average volume invested of {most_traded_sector_volume} USD.")
        
    return message_3


# TODO: tests, error handling
def most_sold_sector_politician(data, selected_politician):
    try:
        most_sold_sector_politician = (data[(data["Politician"] == selected_politician) &
                                           (data["Transaction"] == "Sale") &
                                           (data["quoteType"] == "EQUITY")]
                                  .groupby("sector", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[-1]["sector"])
    except:
        most_sold_sector_politician = "Empty"

    
    try:
        most_sold_sector_volume = (data[(data["Politician"] == selected_politician) &
                                           (data["Transaction"] == "Sale") &
                                           (data["quoteType"] == "EQUITY")]
                                  .groupby("sector", as_index=False)["Invested"]
                                  .sum()
                                  .sort_values(by="Invested", ascending=False)
                                  .iloc[-1]["Invested"])
        
        most_sold_sector_volume = f"{-most_sold_sector_volume:,.0f}"
    except:
        most_sold_sector_volume = "Empty"

    if most_sold_sector_politician == "Empty":
        message_4 = ("They did not perform any sales of EQUITY during the documented time period.")
    else:
        message_4 = (f"{selected_politician} sold EQUITY mostly in {most_sold_sector_politician} sector\
            with the total average volume sold of {most_sold_sector_volume} USD.")
        
    return message_4


# TODO: tests, error handling
def individual_invest_politician(data, list, selected_politician):
    message = []
    for quoteType in list:
        help_df = top_five_purchased_stocks(data, selected_politician, quoteType)
        sub_message = f"in {quoteType}, where the most poular investition is {help_df.iloc[0]['Name']} with a total amount invested of {help_df.iloc[0]['Total Invested']}"
        message.append(sub_message)
    
    final_message = "; ".join(message)

    return final_message


# TODO: tests, error handling
def individual_sell_politician(data, list, selected_politician):
    message = []
    for quoteType in list:
        help_df = top_five_sold_stocks(data, selected_politician, quoteType)
        sub_message = f"in {quoteType}, where the most sold was {help_df.iloc[0]['Name']} with a total amount sold of {help_df.iloc[0]['Total Sold']}"
        message.append(sub_message)
    
    final_message = "; ".join(message)

    return final_message


# TODO: tests, error handling
def section_three_purchase_table(data, list_of_types_of_instruments, selected_politician, purchase, selected_type_of_instrument_section_three):
    if purchase == "Purchase":
        if list_of_types_of_instruments and len(list_of_types_of_instruments) > 0:
            list_of_top_individual_invest = (
                f"{selected_politician} has invested in {', '.join(list_of_types_of_instruments)}. "
                f"They invest {individual_invest_politician(data, list_of_types_of_instruments, selected_politician)}."
            )
            st.write(list_of_top_individual_invest)

            st.caption(f"Displaying the most traded {selected_type_of_instrument_section_three} for {selected_politician}")
            try:
                top_five_table = top_five_purchased_stocks(data, selected_politician, selected_type_of_instrument_section_three)
                st.table(top_five_table)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.write(f"{selected_politician} did not purchase any instruments in the documented time period.")

    elif purchase == "Sale":
        if list_of_types_of_instruments and len(list_of_types_of_instruments) > 0:
            list_of_top_individual_sold = (
                f"{selected_politician} has sold {', '.join(list_of_types_of_instruments)}. "
                f"They sold {individual_sell_politician(data, list_of_types_of_instruments, selected_politician)}."
            )
            st.write(list_of_top_individual_sold)

            st.caption(f"Displaying the most sold {selected_type_of_instrument_section_three} for {selected_politician}")
            try:
                top_five_table_sold = top_five_sold_stocks(data, selected_politician, selected_type_of_instrument_section_three)
                st.table(top_five_table_sold)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.write(f"{selected_politician} did not sell any instruments in the documented time period.")


# TODO: tests, error handling
def five_days(data, selected_politician):
    help_df_purchase = data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")].copy()
    help_df_sale = data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Sale")].copy()

    top_five = (help_df_purchase.groupby("Traded", as_index = False)["Invested"]
                .sum()
                .sort_values(by = "Invested", ascending = False)
                .head(5)
                )
    
    last_five = (help_df_sale.groupby("Traded", as_index = False)["Invested"]
                .sum()
                .sort_values(by = "Invested", ascending = True)
                .head(5)
                )
    
    final = pd.concat([top_five, last_five]).sort_values(by = "Invested")

    return final


# TODO: tests, error handling
def most_active_purchase(data, selected_politician):
    # Prepare and sort data
    help_df = five_days(data, selected_politician)
    help_df = help_df.sort_values(by="Invested", ascending=False)
    
    # Initialize message
    message = f"{selected_politician} has not purchased any instruments during the documented period."
    
    # First part of the message
    if not help_df.empty and help_df.iloc[0]["Invested"] > 0:
        most_active_purchase = help_df.iloc[0]["Traded"]
        most_active_purchase_volume = help_df.iloc[0]["Invested"]
        most_active_purchase_volume = f"{most_active_purchase_volume:,.0f}"
        message_p1 = (
            f"{selected_politician} invested the most on {most_active_purchase} with a total "
            f"volume purchased of {most_active_purchase_volume} USD."
        )
        
        try:
            # Filter data for the most active purchase
            help_df1 = data[
                (data["Politician"] == selected_politician) &
                (data["Traded"] == most_active_purchase) &
                (data["Transaction"] == "Purchase")
            ].copy()

            grouped_df1 = help_df1.groupby("quoteType", as_index=False)["Invested"].sum()

            message_list = [
                f"{quoteType} in a total volume purchased of {grouped_df1[grouped_df1['quoteType'] == quoteType].iloc[0]['Invested']:,.0f} USD"
                for quoteType in grouped_df1["quoteType"].unique()
            ]

            message_p2 = f" The instruments purchased on this day were {'; '.join(message_list)}."

            # Additional sector-specific message for EQUITY
            if "EQUITY" in grouped_df1["quoteType"].unique():
                help_df2 = data[
                    (data["Politician"] == selected_politician) &
                    (data["Traded"] == most_active_purchase) &
                    (data["Transaction"] == "Purchase") &
                    (data["quoteType"] == "EQUITY")
                ].copy()

                grouped_df2 = help_df2.groupby("sector", as_index=False)["Invested"].sum()
                top_3_grouped_df2 = grouped_df2.sort_values(by="Invested", ascending=False).head(3)

                message_list_1 = [
                    f"{sector} in a total volume purchased of {top_3_grouped_df2[top_3_grouped_df2['sector'] == sector].iloc[0]['Invested']:,.0f} USD"
                    for sector in top_3_grouped_df2["sector"]
                ]

                message_p3 = f" On this day, the EQUITY purchased was mainly in the sector: {'; '.join(message_list_1)}."
                message = message_p1 + message_p2 + message_p3
            else:
                message = message_p1 + message_p2

        except (KeyError, IndexError) as e:
            # If any error occurs, fallback to message_p1
            message = message_p1

    return message


# TODO: tests, error handling
def most_active_sell(data, selected_politician):
    help_df = five_days(data, selected_politician)
    help_df = help_df.sort_values(by="Invested", ascending=False)

    # Initialize message
    message = f"{selected_politician} has not sold any instruments during the documented period."

    # First part of the message
    if not help_df.empty and help_df.iloc[-1]["Invested"] < 0:
        most_active_sell = help_df.iloc[-1]["Traded"]
        most_active_sell_volume = -help_df.iloc[-1]["Invested"]
        most_active_sell_volume = f"{most_active_sell_volume:,.0f}"
        message_p1 = (
            f"{selected_politician} sold the most on {most_active_sell} with a total "
            f"volume sold of {most_active_sell_volume} USD."
        )

        try:
            # Filter data for the most active sale
            help_df1 = data[
                (data["Politician"] == selected_politician) &
                (data["Traded"] == most_active_sell) &
                (data["Transaction"] == "Sale")
            ].copy()

            help_df1["Invested"] = -help_df1["Invested"]
            grouped_df1 = help_df1.groupby("quoteType", as_index=False)["Invested"].sum()

            message_list = [
                f"{quoteType} in a total volume sold of {grouped_df1[grouped_df1['quoteType'] == quoteType].iloc[0]['Invested']:,.0f} USD"
                for quoteType in grouped_df1["quoteType"].unique()
            ]

            message_p2 = f" The instruments sold on this day were {'; '.join(message_list)}."

            # Additional sector-specific message for EQUITY
            if "EQUITY" in grouped_df1["quoteType"].unique():
                help_df2 = data[
                    (data["Politician"] == selected_politician) &
                    (data["Traded"] == most_active_sell) &
                    (data["Transaction"] == "Sale") &
                    (data["quoteType"] == "EQUITY")
                ].copy()

                help_df2["Invested"] = -help_df2["Invested"]
                grouped_df2 = help_df2.groupby("sector", as_index=False)["Invested"].sum()

                top_3_grouped_df2 = grouped_df2.sort_values(by="Invested", ascending=False).head(3)
                message_list_1 = [
                    f"{sector} in a total volume sold of {top_3_grouped_df2[top_3_grouped_df2['sector'] == sector].iloc[0]['Invested']:,.0f} USD"
                    for sector in top_3_grouped_df2["sector"]
                ]

                message_p3 = f" On this day, the EQUITY sold was mainly in the sector: {'; '.join(message_list_1)}."
                message = message_p1 + message_p2 + message_p3
            else:
                message = message_p1 + message_p2

        except (KeyError, IndexError) as e:
            # If any error occurs, fallback to message_p1
            message = message_p1

    return message
