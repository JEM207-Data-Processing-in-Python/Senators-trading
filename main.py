#IMPORT LIBRARIES AND PACKAGES
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
from random import randint
from time import sleep
import requests
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


# UPDATE (BOTH INFORMATION ABOUT ASSETS and ALSO SENATORS_TRADING DATASET)
def update_datasets():
    data_trading = pd.read_csv("senators_trading.csv")      #LOADING THE CORE DATASET

    #MISSING IF FOR DIFFERENT DRIVERS
    driver = webdriver.Chrome()         #OPEN DRIVER

    url = "https://trendspider.com/markets/congress-trading/"       #GO TO SENATORS TRADING WEBPAGE
    driver.get(url)
    time.sleep(5)

    headers = driver.find_elements(By.CSS_SELECTOR, "#main-content table thead th")         #OBTAIN HEADERS FOR DATAFRAM
    header_names = [header.text.strip() for header in headers]

    #GET THE DATA FROM THE FIRST PAGE
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, "#main-content table tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text.strip().replace('\n', ' ') for col in cols])


    df = pd.DataFrame(data, columns=header_names)
    df[['Type', 'Amount']] = df['Transaction'].str.extract(r'(\w+)\s\$(.*)')
    df = df.drop(columns=['Transaction', 'Excess return *'])

    last_note = df.iloc[-1]             #SAVE LAST ROW FROM THE TEMPORAL DATASET (WILL BE USED TO CHECK, IF ORIGINAL DATASET CONTAINS THE UPDATED DATA)

    #CONTINUE TO 2nd ... PAGE. CONITINUE UNTIL THE UPDATED DATASET STARTS TO INTERSECT WITH THE ORIGINAL DATASET
    i = 2
    while ((data_trading == last_note).all(axis=1)).any() == False:
        data = []
        check = f'[aria-label="Current Page, Page {i}."]'
        site = f'[aria-label="Go to page {i}."]'
        while driver.find_elements(By.CSS_SELECTOR, check) == []:
            try:
                driver.find_elements(By.CSS_SELECTOR, site)[0].click()
            except Exception as e:
                time.sleep(randint(10,20)/10)
        sleep(randint(10,50)/10)
        rows = driver.find_elements(By.CSS_SELECTOR, "#main-content table tbody tr")
    
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([col.text.strip().replace('\n', ' ') for col in cols])

        help_df = pd.DataFrame(data, columns=header_names)
        help_df[['Type', 'Amount']] = help_df['Transaction'].str.extract(r'(\w+)\s\$(.*)')
        help_df = help_df.drop(columns=['Transaction', 'Excess return *'])

        df = pd.concat([df, help_df])


        i += 1
        last_note = df.iloc[-1]

    driver.quit()
    
    #LEAVE ONLY RECORDS FROM TEMPORAL DATASET, WHICH ARE NOT IN THE ORIGINAL DATASET (CANNOT USE DROP_DUPLICATES DUE TO SIMILARITY BETWEEN SOME TRADES)
    mask = ~df.apply(tuple, axis=1).isin(data_trading.apply(tuple, axis=1))
    result = df[mask]

    #SAVE THE ORIGINAL SYMBOLS FROM THE ORIGINAL CORE DATASET (WHICH CORRESPOND TO THE ORIGINAL DATASET WITH INFO ABOUT STOCKS,ETF,MUTUAL FUNDS...)
    original_symbols = data_trading.Stock.apply(lambda x: x.split(" ")[0]).drop_duplicates()

    #CONNECT TEMPORAL AND CORE DATASET TO GET UP TO DATE DATASET
    data_trading = pd.concat([result, data_trading])

    data_trading.to_csv("senators_trading.csv", index = False)

    #ADD SYMBOLS TO DATASET
    data_trading["ABR"] = data_trading.Stock.apply(lambda x: x.split(" ")[0])

    #GET THE SYMBOLS FROM THE TEMPORAL DATASET AND LEAVE ONLY THOSE ETH,STOCKS..., FOR WHICH THE INFORMATION ARE MISSING
    result["ABR"] = result.Stock.apply(lambda x: x.split(" ")[0])
    result_symbols = result.ABR.drop_duplicates()

    additional_symbols = ~result_symbols.isin(original_symbols)

    #ITTER THROUGH SYMBOLS WITHOUT INFORMATION TO OBTAIN MISSING INFORMATION FROM YAHOO_FINANCE
    #MUST CREATE SEVERAL DATASETS DUE TO DIFFERENCES BETWEEN THE ASSET TYPES
    equity = pd.DataFrame()
    mutual_fund = pd.DataFrame()
    etf = pd.DataFrame()
    other = pd.DataFrame()

    # ITERATE THROUGH SYMBOLS AND GAIN MISSING INFORMATION
    for symbol in additional_symbols:
        try:
            stock = yf.Ticker(symbol)
            time.sleep(randint(10,20)/10)

            stock_info = pd.json_normalize(stock.info)

            if 'quoteType' in stock_info.columns:
                quote_type = stock_info['quoteType'][0]
        
                if quote_type == 'ETF':
                    etf = pd.concat([etf, stock_info], ignore_index=True)
                elif quote_type == 'EQUITY':
                    equity = pd.concat([equity, stock_info], ignore_index=True)
                elif quote_type == 'MUTUALFUND':
                    mutual_fund = pd.concat([mutual_fund, stock_info], ignore_index=True)
                else:
                    other = pd.concat([other, stock_info], ignore_index=True)
            else:
                print(f"quoteType not found for {symbol}. Skipping.")
        except Exception as e:
            continue

    #ORIGINAL DATASET
    info_dataset = pd.read_csv("info_dataset.csv")

    #ETF
    try:
        data_etf = etf[["quoteType", "symbol", "category", "currency"]]
    except:
        data_etf = pd.DataFrame(columns = ["quoteType", "symbol", "category", "currency"])

    #EQUITY
    try:
        data_equity = equity[["quoteType", "symbol", "country", "industry", "sector", "financialCurrency"]]

        data_equity = data_equity.rename(columns = {"industry" : "category", "financialCurrency" : "currency"})
    except:
        data_equity = pd.DataFrame(columns = ["quoteType", "symbol", "country", "industry", "sector", "financialCurrency"])


    #MUTUAL FUND
    try:
        data_mutual_fund = mutual_fund[["quoteType", "symbol", "currency"]]
    except:
        data_mutual_fund = pd.DataFrame(columns = ["quoteType", "symbol", "currency"])

    #OTHER
    try:
        data_other = other[["quoteType", "symbol", "currency"]]
    except:
        data_other = pd.DataFrame(columns = ["quoteType", "symbol", "currency"])

    #MERGE ALL DATASETS TO GET UP TO DATE DATASET WITH INFORMATION ABOUT ASSETS
    info_dataset = pd.concat([info_dataset, data_etf, data_equity, data_mutual_fund, data_other], ignore_index=True, join='outer')

    info_dataset.to_csv("info_dataset.csv", index = False)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATASET PREPARATION

#LOADING THE CORE DATASET
data_trading = pd.read_csv("senators_trading.csv")              #LOAD BOTH DATASETS
info_trading = pd.read_csv("info_dataset.csv")

info_trading = info_trading.drop_duplicates(subset = "symbol")          #SOME DUPLICATES MAY APPEAR

data_trading["Party"] = data_trading["Politician"].str.split(" ").str[-3]           #GATHER IMPORTANT INFORMATION FROM THE NAME (CANNOT BE BUILT-IN CORE DATASET)
data_trading["House"] = data_trading["Politician"].str.split(" ").str[-1]
data_trading["Politician"] = data_trading["Politician"].apply(lambda x: " ".join(x.split(" ")[:-3]))

data_trading["Traded"] = pd.to_datetime(data_trading["Traded"], format="%b %d, %Y")     #CHANGE THE DATETIME FORMAT FOR "TRADED"
data_trading["Traded"] = data_trading["Traded"].dt.strftime("%Y-%m-%d")

data_trading["Filed"] = pd.to_datetime(data_trading["Filed"], format="%b %d, %Y")       #CHANGE THE DATETIME FORMAT FOR "FILED"
data_trading["Filed"] = data_trading["Filed"].dt.strftime("%Y-%m-%d")

data_trading["ABR"] = data_trading["Stock"].apply(lambda x: x.split(" ")[0])            # GATHER ABREVIATIONS FOR THE ASSETS

data_trading["min"] = data_trading["Amount"].str.split(" - \\$").str[0]                 #SPLIT THE RNAGED AMOUNT COLUMN INTO TWO "MIN" AND "MAX" AND DO IMPORTANT CHNAGES
data_trading["max"] = data_trading["Amount"].str.split(" - \\$").str[1]
data_trading["min"] = data_trading["min"].str.replace(",", "")
data_trading["max"] = data_trading["max"].str.replace(",", "")
data_trading["min"] = pd.to_numeric(data_trading["min"], errors="coerce")
data_trading["max"] = pd.to_numeric(data_trading["max"], errors="coerce")


data_trading["avg_invested"] = (data_trading["min"] + data_trading["max"]) / 2          #CALCULATE AVERAGE INVESTMENT SINCE EXACT INVESTMENT IS UNKNOWN

data_trading["avg_invested_adjusted"] = np.where(                                       #CALCULATE ADJUSTED INVESTMENT, SINCE SALE SHOULD DECREASE YOUR TOTAL INVESTED AMOUNT
    data_trading["Type"] == "Purchase",
    (data_trading["min"] + data_trading["max"]) / 2,
    -(data_trading["min"] + data_trading["max"]) / 2
)

data_trading = data_trading.applymap(lambda x: x.strip() if isinstance(x, str) else x)  #DEAL WITH TABULATORS, AND SECRET SYMBOLS IN COLUMNS


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# GRAPH OF ACTIVE INVESTMENT IN TIME

def get_the_color(of_what):                     #FUNCTION THAT SELECTS COLOR FOR REPUBLICANS AND DEMOCRATS (USED IN SOME GRAPHS)
    if of_what == "R":
        color = "red"
    elif of_what == "D":
        color = "blue"

    else:
        get_party = data_trading[data_trading["Politician"] == of_what].iloc[0]["Party"]
        if get_party == "R":
            color = "red"
        elif get_party == "D":
            color = "blue"
    
    return color


def grouping_for_graph(by_what, what_to_display):                       #ALOWS USER TO SEE THE INVESTMENT IN TIME FOR EITHER REP/DEM PARTY, OR FOR SPECIFIC POLITICIAN
    data_trading_in_time = data_trading[[by_what, "Traded", "avg_invested_adjusted"]]

    data_trading_in_time = data_trading_in_time.groupby([by_what, "Traded"]).sum()

    data_trading_in_time.reset_index(inplace=True)

    data_trading_in_time["cumulative_invested"] = (
        data_trading_in_time.sort_values(by=[by_what, "Traded"])                #SORT BY POLITICIAN AND TRADED
        .groupby(by_what)  
        .apply(lambda group: group["avg_invested_adjusted"].cumsum())           #APPLY CUMULATIVE SUM FOR EACH POLITICIAN
        .reset_index(drop=True)  
    )


    help_df = data_trading_in_time[data_trading_in_time[by_what] == what_to_display]

    help_df = help_df.set_index("Traded")

    
    color_of_graph = get_the_color(what_to_display)


    plt.plot(help_df.index, help_df['cumulative_invested'], color = color_of_graph)
    plt.xticks([help_df.index[0], help_df.index[-1]])
    plt.show()

#grouping_for_graph("Politician", "Cory A. Booker")                 #DEMO OF THE PREVIOUS FUNCTION



#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# TABLE OF INFORMATION ABOUT TRADERS

data_trading["ABR"] = data_trading["Stock"].apply(lambda x: x.split(" ")[0])            #GET THE ABREVIATIONS FOR THE ASSETS

data_trading = data_trading.merge(info_trading, how="left", left_on="ABR", right_on="symbol")       #MERGE THE LOG OF TRADING ACTIVITY WITH INFO ABOUT ASSETS


data_trading = data_trading.rename(columns = {"Type" : "Action"})           #RENAMING FOR EASIER WORK
data_trading = data_trading.rename(columns = {"quoteType" : "Type", "category" : "Category", "currency" : "Currency", "country" : "Country", "sector" : "Sector"})

#SOME USEFUL TABLES (MAY BE CREATED BY THE FUNCTION, WILL SEE LATER)
total_purchased = data_trading[data_trading["Action"] == "Purchase"].groupby("Politician")["avg_invested"].sum().reset_index()                          #TOTAL INVESTED
total_sold = data_trading[data_trading["Action"] == "Sale"].groupby("Politician")["avg_invested"].sum().reset_index()                                    #Total SOLD
total_purchased_sector = data_trading[data_trading["Action"] == "Purchase"].groupby(["Politician", "Category"])["avg_invested"].sum().reset_index()        #TOTAL PURCHASED PER SECTOR
total_sold_sector = data_trading[data_trading["Action"] == "Sale"].groupby(["Politician", "Category"])["avg_invested"].sum().reset_index()              #TOTAL SOLD PER SECTOR
total_purchased_type = data_trading[data_trading["Action"] == "Purchase"].groupby(["Politician", "Type"])["avg_invested"].sum().reset_index()           #TOTAL PURCHASED PER TYPE
total_sold_type = data_trading[data_trading["Action"] == "Sale"].groupby(["Politician", "Type"])["avg_invested"].sum().reset_index()                    #TOTAL SOLD PER TYPE
total_purchased_currency = data_trading[data_trading["Action"] == "Purchase"].groupby(["Politician", "Currency"])["avg_invested"].sum().reset_index()       #TOTAL PURCHASED PER CURRENCY
total_sold_currency = data_trading[data_trading["Action"] == "Sale"].groupby(["Politician", "Currency"])["avg_invested"].sum().reset_index()            #TOTAL SOLD PER CURRENCY
total_purchased_country = data_trading[data_trading["Action"] == "Purchase"].groupby(["Politician", "Country"])["avg_invested"].sum().reset_index()     #TOTAL PURCHASED PER COUNTRY
total_sold_country = data_trading[data_trading["Action"] == "Sale"].groupby(["Politician", "Country"])["avg_invested"].sum().reset_index()              #TOTAL SOLD PER COUNTRY

#1 - TWO TYPES FOR THE GRAPHS - EITHER WHEN THE UPPER DATASETS EXIST INDIVIDUALLY
#IF DATASETS EXIST
def pie_chart(df, politician):

    help_df = df[df["Politician"] == politician]

    labels = help_df.iloc[:, 1]

    title = help_df.columns[1]


    plt.figure(figsize=(7, 7))
    plt.pie(help_df['avg_invested'], labels=labels, autopct='%1.1f%%', startangle=0)

    # Add title
    plt.title(f"Average Investment of {politician} by {title} ")

    # Display the pie chart
    plt.show()  

#2 - TWO TYPES FOR THE GRAPHS - EOR THEY DO NOT, AND NEED TO CREATE THEM
#IF DATASETS DO NOT EXIST
def pie_chart_advanced(purchase, subset, politician):

    selected_dataset = data_trading[data_trading["Action"] == purchase].groupby(["Politician", subset])["avg_invested"].sum().reset_index()

    help_df = selected_dataset[selected_dataset["Politician"] == politician]

    labels = help_df.iloc[:, 1]

    title = help_df.columns[1]


    plt.figure(figsize=(7, 7))
    plt.pie(help_df['avg_invested'], labels=labels, autopct='%1.1f%%', startangle=0)

    # Add title
    plt.title(f"Average Investment of {politician} by {title} ")

    # Display the pie chart
    plt.show()  


#pie_chart_advanced("Purchase", "Type", "Adam Kinzinger")                                                        #DEMO OF THE UPPER FUNCTION (2)
#for df in (total_purchased_sector, total_sold_sector, total_purchased_type, total_sold_type,                   #DEMO OF THE UPPER FUNCTION (1)
#           total_purchased_currency, total_sold_currency, total_purchased_country, total_sold_country):
#    pie_chart(df, "Adam Kinzinger")


# TABLE FOR POLITICIANS
#CONTAINT - NAME, HOUSE, PARTY, LAST TRANSACTIONS, PERCENTAGE OF PURCHASED ASSETS


unique_politicians = data_trading[['Politician', "Party", "House"]].drop_duplicates().reset_index(drop=True)            #GET UNIQUE POLITICIANS

# CURRENTLY INVESTED (TOTAL)
data_trading_in_time_politician = data_trading[["Politician", "Traded", "avg_invested_adjusted"]]       #SUBSET OF DATAFRAME

data_trading_in_time_politician = data_trading_in_time_politician.groupby(["Politician", "Traded"]).sum()   #GROUP BY POLITICIAN AND DAY
data_trading_in_time_politician.reset_index(inplace=True)

data_trading_in_time_politician["cumulative_invested"] = (                              #INVESTMENT OF EACH POLITICIAN IN TIME
    data_trading_in_time_politician.sort_values(by=["Politician", "Traded"])            #SORT BY POLITICIAN AND TRADED
    .groupby("Politician")  
    .apply(lambda group: group["avg_invested_adjusted"].cumsum())                       #APPLY CUMULATIVE SUM FOR EACH POLITICIAN
    .reset_index(drop=True)                                                             
)

#LAST TRANSACTION (QUANTITATIVELY)
last_record = data_trading_in_time_politician.sort_values(by=['Politician', 'Traded'], ascending=[True, False]).groupby('Politician').head(1)                    
last_record = last_record.rename(columns = {"cumulative_invested" : "currently_invested", "Traded" : "Last_transaction", "avg_invested_adjusted" : "Action"})
last_record["Action"] = np.where(last_record["Action"] > 0,
    "Purchase",
    "Sale")



# ALL-TIME PERCENTAGE OF INVESTMENT (PER TYPE)

total_purchased_type = data_trading[data_trading["Action"] == "Purchase"].groupby(["Politician", "Type"])["avg_invested"].sum().reset_index()       #ONLY PURCHASED
total_purchased_type_agg = total_purchased_type.groupby("Politician")["avg_invested"].sum().reset_index()                                           
total_purchased_type_agg = total_purchased_type_agg.rename(columns= {"avg_invested" : "total_invested"})


total_purchased_type = total_purchased_type.merge(total_purchased_type_agg, how = "left", on = "Politician")
total_purchased_type["avg_invested"] = total_purchased_type["avg_invested"] / total_purchased_type["total_invested"]        #CALCULATE PERCENTAGE
total_purchased_type = total_purchased_type[["Politician", "Type", "avg_invested"]]
total_purchased_type = total_purchased_type.pivot(index='Politician', columns='Type', values='avg_invested').reset_index()      #PREPARE FOR MERGE



politician_table = unique_politicians.merge(last_record[["Politician", "currently_invested"]], how="left", on = "Politician")       #ADD CURRENTLY INVESTED (AMOUNT)
politician_table = politician_table.merge(last_record[["Politician", "Last_transaction", "Action"]], how="left", on = "Politician")           #ADD LAST TRANSACTION (AMOUNT)
politician_table = politician_table.merge(total_purchased_type, how="left", on = "Politician")                                          #ADD PURCHASES BY TYPE (PERCENTAGE)

#FUNCTION FOR LAST FIVE TRANSACTIONS
def last_five_transactions(politician):
    return (data_trading[data_trading["Politician"] == politician][["ABR", "Stock", "Politician", "Party", "House", "Traded", "Action", "Amount"]]
            .sort_values(by = "Traded", ascending = False)
            .reset_index(drop = True)
            .head(5))