"""
market_api.py

Methods relating to getting data from the market (current price, etc.)
"""

import yfinance as yf

def get_current_price(symbol: str):
	"""
	Get the current price of a whatever identified by a symbol
	"""
	obj = yf.Ticker(symbol)
	return obj.info.regularMarketPrice
