# app/robo_advisor.py

##
## Modules/Packages & Environment
##

import json
import datetime
import csv
import os
import statistics
import sys

from dotenv import load_dotenv
import requests

load_dotenv() #> loads contents of the .env file into the script's environment
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

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
            "open": float(information["1. open"]),
            "high": float(information["2. high"]),
            "low": float(information["3. low"]),
            "close": float(information["4. close"]),
            "volume": float(information["5. volume"]) 
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

def change_rate (a,b):
        return (a-b)/b

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

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

    # Check Internet Connection
    if check_internet() == False:
        print("But, you need to connect to internet. Please try after connecting to online!")
        print("=============================")
        sys.exit()
    else: 
        # User Type-In & Validation (including preliminary validation) 
        while True:
            print("-------------------------")
            symbol = input("Please input a stock symbol (e.g. MSFT, AAPL, AMZN): ")
            
            #Preliminary Validation before parsing
            if symbol.isdigit():
                print("Stock symbols should only cotain alphabets. Please try with valid symbols!")
                continue
            elif len(symbol) > 5:
                print("You input too many characters. Please try with valid symbols!")
                continue
            elif symbol == "":
                print("No input. Please try with valid symbols!")
                continue

            #Validation after parsing                
            else:
                request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
                parsed_response = get_response(symbol)
                if "Error Message" in parsed_response:
                    print("We cannot fild the symbol. Please try with valid stock symbols!")
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

    # WRITE PRICES TO CSV FILE
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")
    write_to_csv(rows, csv_filepath)
    formatted_csv_filepath = csv_filepath.split("../")[1] #> data/prices_"symbol".csv

    ##
    ## RECOMMENDATION
    ##

    decision = ""
    reason = ""
    
    open_prices = [row["open"] for row in rows] #[team["name"] for team in teams]
    close_prices = [row["close"] for row in rows] #[team["name"] for team in teams]
    latest_open = rows[0]["open"]
    latest_high = rows[0]["high"]
    latest_low = rows[0]["low"]

    # Define for Logic 1 - BUY when latest high exceeds last 10-day average high by 3%
    high_prices_10 = [row["high"] for row in rows][:10] #[team["name"] for team in teams]
    avg_high_prices_10 = statistics.mean(high_prices_10)
    threshold_logic1 = 0.03

    # Define for Logic 2 - SELL when latest low is less than last 10-day average low by 3%
    low_prices_10 = [row["low"] for row in rows][:10] #[team["name"] for team in teams]
    avg_low_prices_10 = statistics.mean(low_prices_10)
    threshold_logic2 = -0.02
    #avg_low_prices_10 == 100  #> for testing
    #latest_low = 96  #> for testing

    # Define for Logic 3 - BUY when close price increases three days in a row
    latest_close_1 = rows[1]["close"]
    latest_close_2 = rows[2]["close"]

    # Implementing recommendation logic
    if change_rate(latest_high, avg_high_prices_10) > threshold_logic1:
        decision = "BUY"
        reason = "Logic 1 - Latest high exceeds last 10-day average high by 3%"
        # Result (as of Jun/21/2019 4:37AM)
        # - BUY: AA, FB, HPE, ZTS, T(updated as of Jun/21/2019 6:04pm)
        # - NO BUY: AAPL, AMZN, BRK.A, C, GOOG, KO, LUV, MSFT, T, WMT, CIT, F
    elif change_rate(latest_low, avg_low_prices_10) < threshold_logic2:
        decision = "SELL"
        reason = "Logic 2 - Latest low is less than last 10-day average low by 2%"
        # Result (as of Jun/21/2019 8|:16AM)
        # - SELL: n/a
    elif latest_close > latest_close_1 and latest_close_1 > latest_close_2:
        decision = "BUY"
        reason = "Logic 3 - Close price increases for 3 days in a row"
        # Result (as of Jun/21/2019 8:23AM)
        # - BUY: AMZN, BRK.A, KO, MSFT, GOOG(updated as of Jun/21/2019 6:00pm)
        # - NO BUY: AAPL, C, GOOG, LUV, MSFT, T, WMT, CIT, F
    elif latest_close > avg_high_prices_10:
        decision = "BUY"
        reason = "Logic 4: As latest close price exceeds last 10-day average, \nstock price is expected to go up!"
        # Result (as of Jun/21/2019 6:07PM)
        # - BUY: AAPL, 
        # - NO BUY: C, GOOG, LUV, MSFT, T, WMT, CIT, F
    elif latest_close < avg_low_prices_10:
        decision = "SELL"
        reason = "Logic 5: As latest close price is less than last 10-day average, \nstock price is expected to go up!"
        # Result (as of Jun/21/2019 5:57PM)
        # - SELL: n/a
    else:
        decision = "STAY"
        reason = "No recommendation can be made at this point"

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
    print(f"AVERAGE 10DAYS HIGH: {to_usd(float(avg_high_prices_10))}")
    print(f"AVERAGE 10DAYS LOW: {to_usd(float(avg_low_prices_10))}")

    print("-------------------------")
    print(f"RECOMMENDATION: {decision}!")
    print(f"RECOMMENDATION REASON: {reason}!")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {formatted_csv_filepath}")

    print("-------------------------")
    print("THANK YOU FOR USING ROBO-ADVISOR! \nHAPPY INVESTING!")
    print("=============================")
    print("")



