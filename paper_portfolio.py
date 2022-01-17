#!/usr/bin/env python3
"""
paper_portfolio.py

The `main` executable for this project.
"""

import argparse
from data_types import *
from config import PORTFOLIO_STORAGE_DIR


def parse_args(parser: argparse.ArgumentParser):
    """
	Parse args for our program
	"""
    parser.add_argument("-a",
                        "--action",
                        help="Action to perform.",
                        type=str,
                        choices=act_to_func.keys(),
                        required=True)
    parser.add_argument("-n",
                        "--name",
                        help="Portfolio name to act on",
                        type=str,
                        required=True)
    parser.add_argument(
        "-s",
        "--symbol",
        help=
        "Symbol to use for action, used with buy, sell, check_value options",
        type=str)
    parser.add_argument(
        "-q",
        "--quantity",
        help="Quantity of item being bought, sold, or invested",
        type=str)
    args = parser.parse_args()
    return args


def create(portfolio_name):
    portfolio = Portfolio(
        metadata=PortfolioMetadata(total_cash_entered=0,
                                   date_opened=0,
                                   total_value=0,
                                   portfolio_name=portfolio_name,
                                   settlement_symbol="DOLLAR"))
    json_str = portfolio.to_json()
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "w") as fh:
        fh.write(json_str)


def delete(portfolio_name):
    pass


def invest(portfolio_name, quantity):
    """
	Invest in a portfolio - add money to the settlement fund
	Quantity here is both number of shares in the settlement fund and also price in dollars 
	"""
    pass


def buy(portfolio_name, symbol, quantity):
    pass


def sell(portfolio_name, symbol, quantity):
    pass


def check_value(symbol, quantity):
    pass


def update(portfolio_name):
    pass


if __name__ == '__main__':
    act_to_func = {
        "create": create,
        "delete": delete,
        "invest": invest,
        "buy": buy,
        "sell": sell,
        "check_value": check_value,
        "update": update
    }
    parser = argparse.ArgumentParser(
        description="View and manage paper portfolios")
    args = parse_args(parser)
    act_to_func[args.action](args.name)
