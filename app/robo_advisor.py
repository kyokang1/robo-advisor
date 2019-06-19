
# app/robo_advisor.py

## Modules & Packages


import json


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


#    aapl = json.loads(file_contents)
#    
#    meta = aapl["Meta Data"]
#    last_refreshed = meta["3. Last Refreshed"]
#    
#    daily = aapl["Time Series (Daily)"]
#    latest_data = daily[str(last_refreshed)]
#    latest_closing_price = latest_data["4. close"]
#
#    return latest_closing_price



##
## Input
##

# Intro
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


breakpoint()



##
## Output
##

print("-------------------------")
print(f"SELECTED STOCK: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



