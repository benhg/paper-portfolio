"""
data_types.py

Classes that represent various things in the portfolio
"""

import market_api

class Holding:
    """
    Represents some amount of a stock/bond/ETF/whatever

    Has instance variables for value, price, number held, etc.
    """

    def __init__(self,
                 symbol: str="",
                 quantity: int=0,
                 price: int=None,
                 transactions_list: object=None):
        """
        initialize object
        """
        self.symbol = symbol;
        self.quantity = quantity;
        self.value_held = self.price * self.quantity
        if transactions_list is None:
            transactions_list = []
        if symbol == "DOLLAR":
            price = 1 # DOLLAR is not a valid symbol - we special case it for settlement fund/savings
        elif price is None:
            price = market_api.get_current_price(symbol)
        self.transactions_list = transactions_list
        self.price = price;

    def update_value_held(self):
        """
        Update value held based on current market rate
        """
        self.update_market_price()
        self.value_held = self.price * self.quantity;

    def.update_market_price(self):
        """
        Update our stored price from the market
        """
        if self.symbol != "DOLLAR":
            self.price = market_api.get_current_price(self.symbol)
        return self.price