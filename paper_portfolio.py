#!/usr/bin/env python3
"""
paper_portfolio.py

The `main` executable for this project.
"""

import argparse
from data_types import *
import market_api
from config import PORTFOLIO_STORAGE_DIR

import os


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
    """
    Delete a portfolio
    """
    os.remove(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json")


def invest(portfolio_name, quantity):
    """
	Invest in a portfolio - add money to the settlement fund
	Quantity here is both number of shares in the settlement fund and also price in dollars 
	"""
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "r") as fh:
        portfolio_dict_txt = fh.read()
        portfolio_obj = Portfolio.from_json(portfolio_dict_txt)
        settlement_symbol = portfolio_obj.metadata.settlement_symbol
        portfolio_obj.invest(settlement_symbol, quantity)
        save_to_disk(portfolio_name, portfolio_obj) 


def buy(portfolio_name, symbol, quantity):
    """
    Invest in a portfolio - add money to the settlement fund
    Quantity here is both number of shares in the settlement fund and also price in dollars 
    """
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "r") as fh:
        portfolio_dict_txt = fh.read()
        portfolio_obj = Portfolio.from_json(portfolio_dict_txt)
        settlement_symbol = portfolio_obj.metadata.settlement_symbol
        portfolio_obj.invest(settlement_symbol, quantity)
        save_to_disk(portfolio_name, portfolio_obj) 


def sell(portfolio_name, symbol, quantity):
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "r") as fh:
        portfolio_dict_txt = fh.read()
        portfolio_obj = Portfolio.from_json(portfolio_dict_txt)
        settlement_symbol = portfolio_obj.metadata.settlement_symbol
        portfolio_obj.sell(settlement_symbol, quantity)
        save_to_disk(portfolio_name, portfolio_obj) 


def check_value(symbol, quantity):
    """
    Check value of a specific stock
    """
    return f"Market price of {symbol} : {market_api.get_current_price(symbol)}"

def save_to_disk(portfolio_name, portfolio_obj):
    """
    Save the portfolio to disk 
    """
    json_str = portfolio_obj.to_json()
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "w") as fh:
        fh.write(json_str)

def update(portfolio_name):
    """
    1. Check for dividends
    2. update value in shares
    3. Save portfolio to disk
    """
    with open(f"{PORTFOLIO_STORAGE_DIR}/{portfolio_name}.json", "r") as fh:
        portfolio_dict_txt = fh.read()
        portfolio_obj = Portfolio.from_json(portfolio_dict_txt)
        portfolio_obj.update()
        save_to_disk(portfolio_name, portfolio_obj) 

def print_summary(portfolio_name):
    """
    Print portfolio summary
    """
    pass


if __name__ == '__main__':
    act_to_func = {
        "create": create,
        "delete": delete,
        "invest": invest,
        "buy": buy,
        "sell": sell,
        "check_value": check_value,
        "update": update,
        "print": print_summary
    }
    parser = argparse.ArgumentParser(
        description="View and manage paper portfolios")
    args = parse_args(parser)
    act_to_func[args.action](args.name)
