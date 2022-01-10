"""
data_types.py

Classes that represent various things in the portfolio
"""

import json

import market_api

class Transaction:
    """
    Represents a transaction of some stock/bond/etf

    Positive price is a purchase, negative price is a sale
    Price can be 0 in case of a divident, and has None as from_symbol
    to_symbol is what's being recieved
    from_symbol is what's being spent
    """

    def __init__

class Holding:
    """
    Represents some amount of a stock/bond/ETF/whatever

    Has instance variables for value, price, number held, etc.
    """

    @staticmethod
    def compute_total_gain_loss(obj: Holding):
        """
        Compute the total loss/gain of a Holding
        by iterating through the list of transactions in that holding
        Uses each purchase price used to compute
        """
        pass

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

    def to_json(self) -> str:
        """
        Export this Holding to a JSON object

        Return the JSON string
        """
        self.update_value_held()
        self_dict = {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "value_held":self.value_held,
            "price": self.price,
            "transactions_list": [transaction.to_json() for transaction in self.transactions_list]

        }
        return json.dumps(self_dict)

class Portfolio:
    """
    represents a whole portfolio
    Which is a list of Holdings, plus some metadata
    """
    pass

