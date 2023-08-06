from abc import ABC
from abc import abstractmethod


class Initialize(ABC):

    @abstractmethod
    def __int__(self):
        ...

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def initialize_symbol(self):
        ...
