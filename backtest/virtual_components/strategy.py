from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def get(self):
        """
        Get the features of a strategy
        """
        pass

    @abstractmethod
    def put(self, event):
        """
        Put the latest event of a strategy, like kline, aggTrade, etc
        """
        pass
