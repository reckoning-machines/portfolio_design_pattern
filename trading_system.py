from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PortfolioMeta(ABC):
    _name: str
    _max_gross_notional: float
    _positions: list[int] = field(default_factory=list)

    @abstractmethod
    def add_position(self, *args, **kwargs):
        pass

    @abstractmethod
    def remove_position(self, *args, **kwargs):
        pass


class Portfolio(PortfolioMeta):
    _gross_notional: float = 0

    def add_position(self, Position):
        self._positions.append(Position)
        self._gross_notional = 0
        for p in self._positions:
            self._gross_notional = self._gross_notional + p.notional

    def remove_position(self, Position):
        if Position in self._positions:
            self._positions.remove(Position)

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


class StockMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class Stock(metaclass=StockMeta):
    symbol: str
    _price: float = -1

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError("Price must be a float")
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

PRICES = {"ABC": 53.34, "CFG": 43.30, "DEF": 239.87, "XYZ": 63.45, "YYZ": 27.56}
STOCKS = ["ABC", "CFG", "DEF", "XYZ", "YYZ"]
p = Portfolio("POD-001", 10000000)

for stock in STOCKS:
    s = Stock(stock)
    s.price = PRICES[stock]
    pos = Position(stock=s, notional=100000)
    p.add_position(pos)

print(p.positions)
print(p.gross_notional)
