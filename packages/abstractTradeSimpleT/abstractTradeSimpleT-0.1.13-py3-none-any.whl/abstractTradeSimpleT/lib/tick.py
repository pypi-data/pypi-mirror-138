from abc import ABC
from abc import abstractmethod


class Tick(ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def get_new_tick(self):
        ...
