#robo_advisor_test.py

import os

from app.robo_advisor import to_usd, get_response

def test_to_usd():
    price = 4050.13
    assert to_usd(price) == "$4,050.13"

def test_get_response():
    symbol = "GOOG"
    parsed_response = get_response(symbol)

    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol


