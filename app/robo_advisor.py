# app/robo_advisor.py

## TODO as of Jun/18/2019
# - gitignore
# - buy/sell logic


## Modules & Packages

import json
import datetime
import csv
import os

from dotenv import load_dotenv
import requests

load_dotenv() #> loads contents of the .env file into the script's environment
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(API_KEY)
#breakpoint()

##
## Define Functions
##

def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    response_data = json.loads(response.text)    
    return response_data

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, information in tsd.items():
        row = {
            "timestamp": date,
            "open": information["1. open"],
            "high": information["2. high"],
            "low": information["3. low"],
            "close": information["4. close"],
            "volume": information["5. volume"] 
        }
        rows.append(row)
    return rows

def to_usd(price):  
    return "${0:,.2f}".format(price)

def write_to_csv (rows, csv_filepath):
    with open(csv_filepath, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)
    return True

##
## Main Logic
##

if __name__ == "__main__":       

    ##
    ## Input
    ##

    # Intro
    print("")
    print("=============================")
    print("WELCOME TO ROBO-ADVISOR!")

    # User Type-In & Validation   
    while True:
        print("-------------------------")
        symbol = input("Please input a stock symbol (e.g. MSFT, AAPL, AMZN): ")

        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        #response = requests.get(request_url)
        parsed_response = get_response(symbol)

        if "Error Message" in parsed_response:
            print("Invalid Input! Please try with stock symbols like 'MSFT'!")
            continue
        else:
            break
        
    # Data Transform & Calculation
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    rows = transform_response(parsed_response)
    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] #[team["name"] for team in teams]
    low_prices = [row["low"] for row in rows] #[team["name"] for team in teams]
    recent_high = max(high_prices)
    recent_low = min(low_prices)
    #breakdpoint()

    ##
    ## Processing
    ##

    # WRITE PRICES TO CSV FILE
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")
    write_to_csv(rows, csv_filepath)
    formatted_csv_filepath = csv_filepath.split("../")[1] #> data/prices_"symbol".csv

    # RECOMMENDATION ##TODO


    # etc
    now = datetime.datetime.now()



    ##
    ## DISPLAY Output
    ##

    print("-------------------------")
    print(f"SELECTED STOCK: {symbol}")

    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + str(now.strftime("%Y/%m/%d  %H:%M:%S")))

    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}") #print("LATEST CLOSE: " + to_usd(float(latest_close)))
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")

    print("-------------------------")
    print("RECOMMENDATION: BUY!")
    ## TODO: Recommendation logic
    print("RECOMMENDATION REASON: TODO")
    ## TODO: Recommendation logic
    print(f"WRITING DATA TO CSV: {formatted_csv_filepath}")

    print("-------------------------")
    print("THANK YOU FOR USING ROBO-ADVISOR! \nHAPPY INVESTING!")
    print("=============================")
    print("")



