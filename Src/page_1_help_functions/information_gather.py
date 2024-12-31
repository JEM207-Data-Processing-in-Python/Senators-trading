import streamlit as st
from Src.visualization.tables import top_five_purchased_stocks
from Src.visualization.tables import top_five_sold_stocks


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

def chmaber_politician(data, selected_politician):
    chamber_politician = data[data["Politician"] == selected_politician]["Chamber"].unique()
    if chamber_politician == "House":
        chamber_politician = "House of Representatives"
    elif chamber_politician == "Senate":
        chamber_politician = "Senate"
    else:
        chamber_politician = "Unknown Chamber" 

    return chamber_politician

def first_trade_politician(data, selected_politician):
    first_trade_politician = data[data["Politician"] == selected_politician]["Traded"].min()

    return first_trade_politician

def last_trade_politician(data, selected_politician):
    last_trade_politician = data[data["Politician"] == selected_politician]["Traded"].max()

    return last_trade_politician

def total_invested_politician(data, selected_politician):
    total_invested_politician = data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Purchase")]["Invested"].sum()

    total_invested_politician = f"{total_invested_politician:,.0f}"

    return total_invested_politician

def total_sold_politician(data, selected_politician):
    total_sold_politician = data[(data["Politician"] == selected_politician) & (data["Transaction"] == "Sale")]["Invested"].sum()        

    total_invested_politician = f"{total_sold_politician:,.0f}"
    
    return -total_sold_politician

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

def individual_invest_politician(data, list, selected_politician):
    message = []
    for quoteType in list:
        help_df = top_five_purchased_stocks(data, selected_politician, quoteType)
        sub_message = f"in {quoteType}, where the most poular investition is {help_df.iloc[0]['Name']} with a total amount invested of {help_df.iloc[0]['Total Invested']}"
        message.append(sub_message)
    
    final_message = "; ".join(message)

    return final_message

def individual_sell_politician(data, list, selected_politician):
    message = []
    for quoteType in list:
        help_df = top_five_sold_stocks(data, selected_politician, quoteType)
        sub_message = f"in {quoteType}, where the most sold was {help_df.iloc[0]['Name']} with a total amount sold of {help_df.iloc[0]['Total Sold']}"
        message.append(sub_message)
    
    final_message = "; ".join(message)

    return final_message


def section_three_purchase_table(data, list_of_types_of_instruments, selected_politician, purchase, selected_type_of_instrument_section_three):
    if purchase == "Purchase":
        if list_of_types_of_instruments and len(list_of_types_of_instruments) > 0:
            list_of_top_individual_invest = (
                f"{selected_politician} has invested in {', '.join(list_of_types_of_instruments)}. "
                f"They invest {individual_invest_politician(data, list_of_types_of_instruments, selected_politician)}."
            )
            st.write(list_of_top_individual_invest)

            st.subheader(f"Displaying the most traded {selected_type_of_instrument_section_three} for {selected_politician}")
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

            st.subheader(f"Displaying the most sold {selected_type_of_instrument_section_three} for {selected_politician}")
            try:
                top_five_table_sold = top_five_sold_stocks(data, selected_politician, selected_type_of_instrument_section_three)
                st.table(top_five_table_sold)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.write(f"{selected_politician} did not sell any instruments in the documented time period.")
