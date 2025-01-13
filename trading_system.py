from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import polars as pl


@dataclass
class PortfolioMeta(ABC):
    """
    an abstract class for implementing the portfolio object
    methods to be overwritten
    in the event of different portfolio types
    abstract pattern enforced for system integration
    """

    _name: str
    _max_gross_notional: float
    _positions: dict = field(default_factory=dict)

    @abstractmethod
    def execute_position(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute_trade(self, *args, **kwargs):
        pass

    @abstractmethod
    def pretty_print(self):
        pass


class Portfolio(PortfolioMeta):
    """
    a class to handle a single portfolio
    """

    _gross_notional: float = 0

    def execute_position(self, Position):
        """
        check if position exists
        if position from + to -, execute sell and sell short if needed (raise warning)
        if position does not exists and -, sell short
        check total gross notional against max gross notional and return warning if >
        """

        """
        check if position exists
        """
        if self._positions.get(Position.stock.symbol, None) is not None:
            curr_notional = self._positions[Position.stock.symbol].notional
            new_notional = curr_notional + Position.notional
            """
            To do: check if we flipped
            """
            Position.notional = new_notional
            Position.shares = round(Position.notional / Position.stock.price)

        self._positions[Position.stock.symbol] = Position
        self._gross_notional = 0
        for key in self.positions.keys():
            self._gross_notional = self._gross_notional + self.positions[key].notional
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
        """
        return a polars dataframe of the positions in the portfolio
        """
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

    def execute_trade(self):
        pass


@dataclass
class StockMeta(ABC):
    """
    abstract class for a stock
    design enforced for system integration in case of different types of stocks
    """

    _symbol: str
    _price: str


@dataclass
class Stock(StockMeta):
    """
    a class to handle a single type of stock object
    """

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
    """
    abstract class for a stock and what the portfolio manager wants to do with it
    """

    stock: Stock
    notional: Optional[float] = None
    shares: Optional[int] = None

    def __post_init__(self):
        pass

    def calculate_shares(self):
        pass


@dataclass
class Position(PositionMeta):
    """
    a single position type with some error checks
    """

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
client code goes here
"""

if __name__ == "__main__":

    """
    here the client would build a portfolio object
    (perhaps after polling the existing positions in a portfolio system)
    """
    print("instantiate portfolio")

    PRICES = {"ABC": 53.34, "CFG": 43.30, "DEF": 239.87, "XYZ": 63.45, "YYZ": 27.56}
    STOCKS = ["ABC", "CFG", "DEF", "XYZ", "YYZ"]
    clsPortfolio = Portfolio("POD-001", 10000000)
    for stock in STOCKS:
        clsStock = Stock(stock)
        clsStock.price = PRICES[stock]
        """
        add new position to portfolio
        """
        pos = Position(stock=clsStock, notional=100000)
        clsPortfolio.execute_position(pos)

    """
    pretty_print returns a polars dataframe of the positions in the book
    """
    print(clsPortfolio.pretty_print())

    """
    short DEF
    """
    print("short DEF")
    stock_symbol = "DEF"
    clsStock = Stock(stock_symbol)
    clsStock.price = PRICES[stock_symbol]
    pos = Position(clsStock, notional=-200000)
    clsPortfolio.execute_position(pos)
    print(clsPortfolio.pretty_print())
