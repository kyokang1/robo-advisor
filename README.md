# K-young's "Robo Advisor"

## Summary

Welcome to Robo-Advisor Investment Tool developed by K-young. This "Robo Advisor" project will make recommendation on stock purchase or sell based on the pre-implemented logic. The data is updated on real-time basis using AlphaVantage Stock Market API. If the stock information matches with one of the recommendation logics, the system will give you the investment recommendation such as `"BUY"` or `"SELL"`. If there is no recommendation logic applied, you will receive `"STAY"` recommendation.


## Set-up

### Prerequisites

It is recommended to set up a virtual environment to ensure Python runs under the following prerequisites:
  + Anaconda 3.7
  + Python 3.7
  + Pip

### Installation

Install pip command to install the packages required to run the program. You can run the following command in command line:
```
pip install pytest # (only if you'll be writing tests)
pip install -r requirements.txt
```

The required packages are as follows:
```
requests
python-dotenv
```

### AlphaVantage API

As the program fetches real-time stock information using AlphaVantage API, the user needs API Key to use the API and run the program. Please [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "abc123") in the link.

After obtaining an API Key, you need to input your API Key in the file ".env" to specify your real API Key like below:

    ALPHAVANTAGE_API_KEY="abc123"

Please note that the ".env" is ignored from the version control using [].gitignore](/.gitignore) file for security purpose. ".gitignore" prevents the ".env" file and its secret credentials from being tracked in version control. 


## Usage

### Run the app

Use your text editor or the command-line to run the recommendation script like below:

```py
python app/robo_advisor.py
```

Please make sure to run the app in the internet connected. Otherwise you would not be able to fetch the data and see an alert message to go online.

The system will parse the latest price information of the stock you input. Please make sure you input the valid stock symbols such as (e.g. `"MSFT, AAPL, GOOG, AMZN"`). If you input invalid stock symbols `containing numbers`, symbols `exceeding 5 characters`, or `do not input`, the system will generate error messages until you input valid inputs. 

Price information will be stored in the 'data' directory as CSV file and each file is named with corresponding to the given stock symbol (e.g. "data/prices_msft.csv, "prices_aapl.csv", etc.).

### Testing

The program has the function to run automated test to see if the program runs as designed. 

Firstly, you need to nstall pytest if you do not install pytest package in the virtual environment. 
    (Note: This is the first time only. You do not need to run this next time.):

```sh
pip install pytest
```

After the installation, you can run the pytest with the simple script like below:
```sh
pytest
```

The designed tests are as follows:
```sh
test_to_usd  
-> Test various scenarios to ensure the price formatting function displays a dollar sign, 
   two decimal places, and a thousands separator.

test_get_response
-> Test to ensure the function returns the expected response data in a usable format 
   (i.e. a dictionary with keys "Meta Data" and "Time Series (Daily)").
```

## Recommendation Logic

The followings are the recoomendation logic on the stocks you input:

  1. Logic 1 - BUY when latest high exceeds last 10-day average high by 3%
  2. Logic 2 - SELL when latest low is less than last 10-day average low by 1.5%
  3. Logic 3 - BUY when close price increases three days in a row
  4. Logic 4 - BUY when latest close price exceeds last 10-day average high
  5. Logic 5 - SELL when latest close price is less than last 10-day average low

If the stock meets one of the recommendation, the system will dsiplay the recommended decision of `"BUY"` or `"SELL"`. Logic 1 through 5 is implemented in sequence depending on the importance or impact of recommendation. For example, the stock `"AMZN"` matches the recommendation logic 1 and 3, the system will give you `"BUY"` decision with the reason of `Logic 1 - BUY when latest high exceeds last 10-day average high by 3%`. 

If there is no matching recoomendation logic, you will see `"Stay"` (a.k.a. No Recommendation) recoomendation.

More recommendation logics will be implemented in the following versions. If you have any great idea on the recommendation logic, please feel free to reach out to me. K-young will be more than happy to implement the logic in the Robo-Advisor. 

## [License](/LICENSE.md)

Hope the tool helps your wise investing! Thank you for using!
