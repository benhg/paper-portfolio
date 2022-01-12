"""
data_types.py

Classes that represent various things in the portfolio
"""

import datetime
import json
from enum import Enum, auto

import market_api

class Type(Enum):
    Sell = auto()
    Buy = auto()
    Dividend = auto()
    Split = auto()
    Type_Max = auto()



class Transaction:
    """
    Represents a transaction of some stock/bond/etf

    Price can be 0 in case of a dividend, and has None as from_symbol
    to_symbol is what's being recieved
    from_symbol is what's being spent
    TODO: think about how to handle splits.
    """

    @staticmethod
    def from_json(json_txt):
        dict_self = json.loads(json_txt)
        return Transaction(to_symbol=dict_self["to_symbol"],
                           from_symbol=dict_self["from_symbol"],
                           price=dict_self["price"],
                           quantity=dict_self["quantity"],
                           xaction_type=dict_self["xaction_type"])


    def __init__(self,
                 to_symbol="",
                 from_symbol="",
                 price=0,
                 quantity=0,
                 xaction_type=Type_Max):
        self.to_symbol = to_symbol
        self.from_symbol = from_symbol
        self.price = price
        self.quantity = quantity
        self.type = xaction_type


    def to_json(self):
        self_dict = {
            "to_symbol": self.to_symbol,
            "from_symbol": self.from_symbol,
            "price": self.price,
            "quantity": self.quantity,
            "type": self.type
        }
        return json.dumps(self_dict)

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

    @staticmethod
    def from_json(json_txt):
        return Holding()

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
        self.last_updated = datetime.date.today

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

    def check_for_dividends(self):
        """
        Check whether a dividend has been issued since this holding was last updated
        If so, adjust holding's "quantity" and "value_held" to reflect this
        """
        pass

class PortfolioMetadata:

    @staticmethod
    def from_json():
        pass

    def __init__():
        pass

    def to_json():
        pass

class Portfolio:
    """
    represents a whole portfolio
    Which is a list of Holdings, plus some metadata
    """

    @staticmethod
    def from_json(json_txt):
        return Portfolio()

    def __init__(self,
                 metadata=PortfolioMetadata(),
                 portfolio_name="",
                 ):
        pass

    def to_json():
        pass


