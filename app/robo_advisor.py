
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



