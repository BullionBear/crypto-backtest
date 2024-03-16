import pandas as pd

from abc import ABC, abstractmethod
from backtest.models import KLine


class KLineIterator(ABC):

    @abstractmethod
    def __next__(self) -> KLine:
        """Return the next item in the sequence. On reaching the end, raise StopIteration."""
        pass

    def __iter__(self):
        """Return the iterator object itself."""
        return self

    def to_dataframe(self):
        klines = [dict(kline) for kline in self]
        return pd.DataFrame(klines)
