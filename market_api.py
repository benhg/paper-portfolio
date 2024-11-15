"""
market_api.py

Methods relating to getting data from the market (current price, etc.)
"""

import yfinance as yf

import datetime


def get_current_price(symbol: str):
    """
    Get the current price of a whatever identified by a symbol
    """
    obj = yf.Ticker(symbol)
    return obj.info["currentPrice"]


def get_last_dividend_date(symbol: str):
    """
    Get the last date that a dividend was exercised
    """
    obj = yf.Ticker(symbol)
    return datetime.date.fromtimestamp(obj.info.lastDividendDate)


def get_last_dividend_value(symbol: str):
    """
    Get the value of the last dividend, measured in number of shares
    """
    obj = yf.Ticker(symbol)
    last_dividend_date = datetime.date.fromtimestamp(obj.info.lastDividendDate)
    next_week = datetime.date.fromtimestamp(
        (obj.info.lastDividendDate + (24 * 3600 * 7)))
    history = obj.history(start=last_dividend_date, end=next_week)
    share_price = history.iloc[0]["Close"]
    dividend_cash_value = obj.lastDividendValue
    return (dividend_cash_value / share_price)
