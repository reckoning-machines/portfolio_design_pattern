from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import polars as pl


@dataclass
class PortfolioMeta(ABC):
    _name: str
    _max_gross_notional: float
    _positions: dict = field(default_factory=dict)

    @abstractmethod
    def execute_position(self, *args, **kwargs):
        pass

    def pretty_print(self):
        pass


class Portfolio(PortfolioMeta):
    _gross_notional: float = 0

    def execute_position(self, Position):
        """
        check if position exists
        if position from + to -, execute sell and sell short if needed
        if position does not exists and -, sell short
        check total gross notional against max gross notional and return warning if >
        """
        self._positions[Position.stock.symbol] = Position
        self._gross_notional = 0
        for key in self._positions.keys():
            self._gross_notional = self._gross_notional + self._positions[key].notional
        if self._gross_notional > self._max_gross_notional:
            print(
                f"Portfolio gross {self._gross_notional} is over max gross notional: {self._max_gross_notional}"
            )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

    @property
    def positions(self):
        return self._positions

    @property
    def max_gross_notional(self):
        return self._max_gross_notional

    @max_gross_notional.setter
    def name(self, value):
        if not isinstance(value, float):
            raise TypeError("Max gross notional must be a float")
        self._max_gross_notional = value

    @property
    def positions(self):
        return self._positions.copy()

    @property
    def gross_notional(self):
        return self._gross_notional

    def pretty_print(self):
        print_dict = {}
        symbol_list = []
        shares_list = []
        notional_list = []
        price_list = []
        for key in clsPortfolio.positions:
            symbol_list.append(clsPortfolio.positions[key].stock.symbol)
            shares_list.append(clsPortfolio.positions[key].shares)
            notional_list.append(clsPortfolio.positions[key].notional)
            price_list.append(clsPortfolio.positions[key].stock.price)
        print_dict["symbol"] = symbol_list
        print_dict["shares"] = shares_list
        print_dict["notional"] = notional_list
        print_dict["price"] = price_list
        df = pl.DataFrame(print_dict)
        df = df.sort("notional")
        return df


@dataclass
class StockMeta(ABC):
    _symbol: str
    _price: str


@dataclass
class Stock(StockMeta):
    _symbol: str
    _price: float = -1

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError("Price must be a float")
        self._price = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if not isinstance(value, str):
            """
            more validation can go here,
            like restricted list or is a valid traded symbol
            """
            raise TypeError("Symbol must be a string")
        self._price = value


@dataclass
class PositionMeta(ABC):
    stock: Stock
    notional: Optional[float] = None
    shares: Optional[int] = None

    def __post_init__(self):
        pass

    def calculate_shares(self):
        pass


@dataclass
class Position(PositionMeta):
    stock: Stock = None
    notional: float = None
    shares: int = None

    def __post_init__(self):
        if self.notional is None and self.shares is None:
            raise TypeError("At least one of notional or shares must be set")
        self.calculate_shares()

    def calculate_shares(self):
        if self.shares is None:
            self.shares = round(self.notional / self.stock.price, 0)


"""
client code
"""
if __name__ == "__main__":

    PRICES = {"ABC": 53.34, "CFG": 43.30, "DEF": 239.87, "XYZ": 63.45, "YYZ": 27.56}
    STOCKS = ["ABC", "CFG", "DEF", "XYZ", "YYZ"]
    clsPortfolio = Portfolio("POD-001", 10000000)

    for stock in STOCKS:
        clsStock = Stock(stock)
        clsStock.price = PRICES[stock]
        pos = Position(stock=clsStock, notional=100000)
        clsPortfolio.execute_position(pos)

    print(clsPortfolio.pretty_print())
