from abc import ABC
from abc import abstractmethod


class Trade(ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def open_buy(self):
        ...

    @abstractmethod
    def open_sell(self):
        ...

    @abstractmethod
    def position_open(self):
        ...

    @abstractmethod
    def position_close(self):
        ...

    @abstractmethod
    def check_position(self):
        ...
