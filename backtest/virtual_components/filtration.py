from abc import ABC, abstractmethod


class Filtration(ABC):
    @abstractmethod
    def get(self) -> dict[str, float]:
        """
        Get the features of a strategy
        """
        pass

    @abstractmethod
    def put(self, event: dict[str, float]):
        """
        Put the latest event of a strategy, like kline, aggTrade, etc
        """
        pass
