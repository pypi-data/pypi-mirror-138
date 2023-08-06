from abc import ABC
from abc import abstractmethod


class TimeFrame(ABC):

    @abstractmethod
    def __init__(self):

        self.ONE_MINUTE = ...  # 1 minute
        self.TWO_MINUTES = ...  # 2 minutes
        self.THREE_MINUTES = ...  # 3 minutes
        self.FOUR_MINUTES = ...  # 4 minutes
        self.FIVE_MINUTES = ...  # 5 minutes
        self.SIX_MINUTES = ...  # 6 minutes
        self.TEN_MINUTES = ...  # 10 minutes
        self.TWELVE_MINUTES = ...  # 12 minutes
        self.FIFTEEN_MINUTES = ...  # 15 minutes
        self.TWENTY_MINUTES = ...  # 20 minutes
        self.THIRTY_MINUTES = ...  # 30 minutes
        self.ONE_HOUR = ...  # 1 hour
        self.TWO_HOURS = ...  # 2 hour
        self.THREE_HOURS = ...  # 3 hour
        self.FOUR_HOURS = ...  # 4 hour
        self.SIX_HOURS = ...  # 6 hour
        self.EIGHT_HOURS = ...  # 8 hour
        self.TWELVE_HOURS = ...  # 12 hour
        self.ONE_DAY = ...  # 1 Day
        self.THREE_DAY = ...  # 3 Days
        self.ONE_WEEK = ...  # 1 Week
        self.ONE_MONTH = ...  # 1 Month
