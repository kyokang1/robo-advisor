
# app/robo_advisor.py

## Modules & Packages


import json
import datetime

import requests


##
## Data Load
##


def get_response(symbol):
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
    response = requests.get(request_url)
    response_data = json.loads(response.text)    
    return response_data

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, daily_prices in tsd.items():
        row = {
            "date": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"] 
        }
        rows.append(row)
    return rows

def to_usd(price):  
    return "${0:,.2f}".format(price)


##
## Input
##

# Intro
print("")
print("=============================")
print("WELCOME TO ROBO-ADVISOR!")

# User Type-In
print("-------------------------")
symbol = input("Please input a stock symbol (e.g. MSFT, AAPL, AMZN): ")
## TODO: Validate the symbol

parsed_response = get_response(symbol)
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
#breakpoint()

rows = transform_response(parsed_response)
latest_close = rows[0]["close"]
high_prices = [row["high"] for row in rows] #[team["name"] for team in teams]
low_prices = [row["low"] for row in rows] #[team["name"] for team in teams]
recent_high = max(high_prices)
recent_low = min(low_prices)

#breakpoint()



##
## Output
##

print("-------------------------")
print(f"SELECTED STOCK: {symbol}")

print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
now = datetime.datetime.now()
print("REQUEST AT: " + str(now.strftime("%Y/%m/%d  %H:%M:%S")))

print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") #print("LATEST CLOSE: " + to_usd(float(latest_close)))
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")

print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")

print("-------------------------")
print("THANK YOU FOR USING ROBO-ADVISOR! \nHAPPY INVESTING!")
print("=============================")
print("")



