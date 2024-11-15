"""
data_types.py

Classes that represent various things in the portfolio
"""

import datetime
import json
from enum import IntEnum, auto

import market_api


class InvestmentException(Exception):
    """
    Error class.
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f"<InvestmentException msg={self.msg}>"


class InvestmentType(IntEnum):
    Sell = 0
    Buy = 1
    Dividend_Reinvest = 2
    Dividend_Settle = 3
    Split = 4
    Investment = 5
    Withdrawl = 6
    InvestmentType_Max = 7


class DividendBehavior(IntEnum):
    Reinvest = 0
    Settlement = 1


class Holding:
    """
    Represents some amount of a stock/bond/ETF/whatever

    Has instance variables for value, price, number held, etc.
    """

    @staticmethod
    def from_json(json_txt):
        dict_self = json.loads(json_txt)
        return Holding(symbol=dict_self["symbol"],
                       quantity=dict_self["quantity"],
                       price=dict_self["price"],
                       last_updated=dict_self["last_updated"],
                       dividend_behavior=dict_self["dividend_behavior"],
                       transactions_list=[
                           Transaction.from_json(json.dumps(t))
                           for t in dict_self["transactions_list"]
                       ])

    def __init__(self,
                 symbol: str = "",
                 quantity: int = 0,
                 price: int = 0,
                 last_updated: str = "",
                 transactions_list: object = None,
                 dividend_behavior=DividendBehavior.Reinvest):
        """
        initialize object
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.value_held = self.price * self.quantity
        if transactions_list is None:
            transactions_list = []
        if symbol == "DOLLAR":
            price = 1  # DOLLAR is not a valid symbol - we special case it for settlement fund/savings
        else:
            price = market_api.get_current_price(symbol)
        self.transactions_list = transactions_list
        self.last_updated = last_updated
        self.dividend_behavior = dividend_behavior

    def update_value_held(self):
        """
        Update value held based on current market rate
        """
        self.update_market_price()
        self.value_held = self.price * self.quantity

    def update_market_price(self):
        """
        Update our stored price from the market
        """
        if self.symbol != "DOLLAR":
            self.price = market_api.get_current_price(self.symbol)
        else:
            self.price == 1
        return self.price

    def to_json(self) -> str:
        """
        Export this Holding to a JSON object

        Return the JSON string
        """
        self.update_value_held()
        self_dict = {
            "symbol":
            self.symbol,
            "quantity":
            self.quantity,
            "value_held":
            self.value_held,
            "price":
            self.price,
            "last_updated":
            datetime.date.today().strftime("%Y-%m-%d"),
            "dividend_behavior":
            self.dividend_behavior,
            "transactions_list":
            [transaction.to_json() for transaction in self.transactions_list]
        }
        return self_dict

    def compute_total_gain_loss(self):
        """
        Compute the total loss/gain of a Holding
        by iterating through the list of transactions in that holding
        Uses each purchase price used to compute
        """
        pass

    def check_for_dividends(self):
        """
        Check whether a dividend has been issued since this holding was last updated
        If so, adjust holding's "quantity" and "value_held" to reflect this

        returns amount to add to settlement fund
        """
        dollars = 0
        shares = 0
        last_dividend_date = market_api.get_last_dividend_date(self.symbol)
        last_updated = datetime.datetime.strptime(self.last_updated,
                                                  "%Y-%m-%d").date()
        if last_updated < last_dividend_date:
            # Do the update. Get the share value in number of shares, assume we reinvest
            shares = market_api.get_last_dividend_value(
                self.symbol) * self.shares
            if self.dividend_behavior == DividendBehavior.Reinvest:
                self.quantity += shares
            elif self.dividend_behavior == DividendBehavior.Settlement:
                self.update_market_price()
                dollars = shares * self.price
        else:
            return 0

        dividend_type = InvestmentType.Dividend_Reinvest if self.dividend_behavior == DividendBehavior.Reinvest else InvestmentType.Dividend_Settle
        to_symbol = self.symbol if self.dividend_behavior == DividendBehavior.Reinvest else "DOLLAR"
        from_symbol = self.symbol

        self.transactions_list.append(
            Transaction(to_symbol=to_symbol,
                        from_symbol=from_symbol,
                        price=self.price,
                        quantity=shares,
                        xaction_type=dividend_type,
                        date=datetime.date.today().strftime("%Y-%m-%d")))

        self.update_value_held()
        return dollars

    def __repr__(self):
        return str(self.to_json())


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
                           xaction_type=dict_self["xaction_type"],
                           date=dict_self["date"])

    def __init__(self,
                 to_symbol="",
                 from_symbol="",
                 price=0,
                 quantity=0,
                 xaction_type=InvestmentType.InvestmentType_Max,
                 date=datetime.date.today().strftime("%Y-%m-%d")):
        self.to_symbol = to_symbol
        self.from_symbol = from_symbol
        self.price = price
        self.quantity = quantity
        self.type = xaction_type
        self.date = date

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        self_dict = {
            "to_symbol": self.to_symbol,
            "from_symbol": self.from_symbol,
            "price": self.price,
            "quantity": self.quantity,
            "xaction_type": self.type,
            "date": self.date
        }
        return self_dict

    def __repr__(self):
        return str(self.to_json())


class PortfolioMetadata:
    """
    Wrapper class to hold metadata about a portfolio
    """

    @staticmethod
    def from_json(json_txt):
        self_dict = json.loads(json_txt)
        return PortfolioMetadata(
            total_cash_entered=int(self_dict["total_cash_entered"]),
            date_opened=self_dict["date_opened"],
            date_last_accessed=datetime.date.today().strftime("%Y-%m-%d"),
            total_value=self_dict["total_value"],
            settlement_symbol=self_dict["settlement_symbol"],
            portfolio_name=self_dict["portfolio_name"],
            total_cash_withdrawn=self_dict["total_cash_withdrawn"],
            dividend_behavior=self_dict["dividend_behavior"])

    def __init__(self,
                 total_cash_entered=0,
                 date_opened=0,
                 total_value=0,
                 portfolio_name="",
                 settlement_symbol="",
                 date_last_accessed=0,
                 total_cash_withdrawn=0,
                 dividend_behavior=DividendBehavior.Reinvest):
        self.total_cash_entered = total_cash_entered
        self.date_opened = date_opened
        self.date_last_accessed = datetime.date.today().strftime("%Y-%m-%d")
        self.total_value = total_value
        self.portfolio_name = portfolio_name
        self.settlement_symbol = settlement_symbol
        self.total_cash_withdrawn = total_cash_withdrawn
        self.dividend_behavior = dividend_behavior

    @property
    def gain_loss(self):
        # Total gain/loss over the history of the account
        return self.total_value - self.total_cash_entered

    def update_last_accessed_date(self):
        self.date_last_accessed = datetime.date.today().strftime("%Y-%m-%d")

    def to_json(self):
        self_dict = {
            "total_cash_entered": self.total_cash_entered,
            "total_cash_withdrawn": self.total_cash_withdrawn,
            "date_opened": self.date_opened,
            "date_last_accessed": self.date_last_accessed,
            "total_value": self.total_value,
            "portfolio_name": self.portfolio_name,
            "settlement_symbol": self.settlement_symbol,
            "dividend_behavior": self.dividend_behavior
        }
        return self_dict

    def __repr__(self):
        return str(self.to_json())


class Portfolio:
    """
    represents a whole portfolio
    Which is a list of Holdings, plus some metadata
    """

    @staticmethod
    def from_json(json_txt):
        self_dict = json.loads(json_txt)
        return Portfolio(metadata=PortfolioMetadata.from_json(
            json.dumps(self_dict["metadata"])),
                         holdings_list={
                             h.get("symbol"): Holding.from_json(json.dumps(h))
                             for h in self_dict["holdings_list"].values()
                         })

    def compute_total_gain_loss(self):
        gain_loss = 0
        for holding in self.holdings_list.values():
            gain_loss += Holding.compute_total_gain_loss(holding)
        return gain_loss

    def __init__(self,
                 metadata=PortfolioMetadata(total_cash_entered=0,
                                            date_opened=0,
                                            total_value=0,
                                            portfolio_name="",
                                            settlement_symbol="DOLLAR"),
                 holdings_list=None):
        self.metadata = metadata
        self.holdings_list = {}
        if holdings_list is not None:
            self.holdings_list = holdings_list

    def to_json(self):
        self_dict = {
            "metadata": self.metadata.to_json(),
            "holdings_list": {
                h.symbol: h.to_json()
                for h in self.holdings_list.values()
            }
        }
        return self_dict

    def __repr__(self):
        return str(self.to_json())

    def invest(self, symbol, amount):
        """
        Invest <amount> of shares in <symbol>

        If <symbol> doesn't exist, add to list

        If <symbol> is not <self.settlement_symbol>, subtract equivalent today dollars from settlement
        """

        if amount == 0:
            return

        if self.metadata.settlement_symbol == symbol:
            self.metadata.total_cash_entered += amount
            self.holdings_list[symbol].value_held += (amount)
            self.holdings_list[symbol].quantity += (amount)
            self.holdings_list[symbol].transactions_list.append(
                Transaction(to_symbol=symbol,
                            from_symbol="",
                            price=amount,
                            quantity=amount,
                            xaction_type=InvestmentType.Investment,
                            date=datetime.date.today().strftime("%Y-%m-%d")))
            return

        holding = self.holdings_list.get(symbol, Holding(symbol=symbol))
        holding.update_value_held()
        set_holding = self.holdings_list[self.metadata.settlement_symbol]
        # Don't need to update value because price is always 1
        if set_holding.value_held < (amount * holding.price):
            raise InvestmentException("Not Enough Money!")
        set_holding.value_held -= (amount * holding.price)
        holding.value_held += (amount * holding.price)
        holding.quantity += amount

        holding.transactions_list.append(
            Transaction(to_symbol=symbol,
                        from_symbol=self.metadata.settlement_symbol,
                        price=holding.price,
                        quantity=amount,
                        xaction_type=InvestmentType.Buy,
                        date=datetime.date.today().strftime("%Y-%m-%d")))

        holding.update_value_held()

        self.holdings_list[self.metadata.settlement_symbol] = set_holding
        self.holdings_list[symbol] = holding

    def update(self):
        """
        For each holding:
        - Update price
        - Check for dividends
        - update total gain/loss
        """
        for key, holding in self.holdings_list.items():
            if (key == self.metadata.settlement_symbol):
                continue
            dollars = self.holdings_list[key].check_for_dividends()
            self.invest(self.metadata.settlement_symbol, dollars)
            self.holdings_list[key].update_value_held()

    def sell(self, symbol, amount):
        """
        Sell <amount> of shares in <symbol>. Add equivalent today dollars to settlement.
        """
        if amount == 0:
            return

        if self.metadata.settlement_symbol == symbol:
            self.metadata.total_cash_withdrawn += amount
            self.holdings_list[symbol].value_held -= (amount)
            self.holdings_list[symbol].quantity -= (amount)
            self.holdings_list[symbol].transactions_list.append(
                Transaction(to_symbol=symbol,
                            from_symbol="",
                            price=amount,
                            quantity=amount,
                            xaction_type=InvestmentType.Withdrawl,
                            date=datetime.date.today().strftime("%Y-%m-%d")))
            return

        if symbol not in self.holdings_list.keys():
            raise InvestmentException(f"None of {symbol} owned!")

        holding = self.holdings_list.get(symbol, Holding(symbol=symbol))
        holding.update_value_held()

        if amount > holding.quantity:
            raise InvestmentException(f"Not enogh of {symbol} owned!")

        set_holding = self.holdings_list[self.metadata.settlement_symbol]
        set_holding.quantity += amount
        holding.value_held -= (amount * holding.price)
        holding.transactions_list.append(
            Transaction(to_symbol=self.metadata.settlement_symbol,
                        from_symbol=symbol,
                        price=holding.price,
                        quantity=amount,
                        xaction_type=InvestmentType.Sell,
                        date=datetime.date.today().strftime("%Y-%m-%d")))
        holding.quantity -= amount

        holding.update_value_held()

        self.holdings_list[self.metadata.settlement_symbol] = set_holding
        self.holdings_list[symbol] = holding
