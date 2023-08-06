from enum import Enum
from typing import List
from dataclasses import dataclass
from mashumaro import DataClassJSONMixin

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"

@dataclass
class CurrencyPosition(DataClassJSONMixin):
    currency: Currency
    balance: float

@dataclass
class StockPosition(DataClassJSONMixin):
    ticker: str
    name: str
    balance: int

@dataclass
class Portfolio(DataClassJSONMixin):
    currencies: List[CurrencyPosition]
    stocks: List[StockPosition]

my_portfolio = Portfolio(
    currencies=[
        CurrencyPosition(Currency.USD, "238.67"),
        CurrencyPosition(Currency.EUR, "10"),
        StockPosition("AAPL", "Apple", "10"),
    ],
    stocks=[
        StockPosition("AAPL", "Apple", "10"),
        StockPosition("AMZN", "Amazon", "10"),
    ]
)

json_string = my_portfolio.to_json()
print(json_string)
print(Portfolio.from_json(json_string))  # same as my_portfolio
