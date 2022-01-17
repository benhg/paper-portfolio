#!/usr/bin/env python3
"""
paper_portfolio.py

The `main` executable for this project.
"""

import argparse

PARSER_ACTION_CHOICES = ["create", "delete", "invest", "buy", "sell", "check_value", "update"]

def parse_args(parser: argparse.ArgumentParser):
	"""
	Parse args for our program
	"""
	parser.add_argument("-a", "--action", help="Action to perform: Choices: {}".format('\n\t'.join(PARSER_ACTION_CHOICES)), type=str, choices=PARSER_ACTION_CHOICES, required=True)
	parser.add_argument("-n", "--name", help="Portfolio name to act on", type=str, required=True)
	parser.add_argument("-s", "--symbol", help="Symbol to use for action, used with buy, sell, check_value options", type=str)
	parser.add_argument("-q", "--quantity", help="Quantity of item being bought, sold, or invested", type=str)
	args = parser.parse_args()
	return args


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="View and manage paper portfolios")
	args = parse_args(parser)