from typing import List
import talib
from backtest.virtual_components import Filtration
from backtest.models import KLine


class SMAFiltration(Filtration):
    def __init__(self, n: int):
        self._klines: List[KLine] = []
        self.n = n

    def get(self):
        close = [kline.close for kline in self._klines[-self.n:]]
        return talib.SMA(close, timeperiod=self.n)[-1]

    def put(self, event: KLine):
        self._klines.append(event)
        if len(self._klines) > self.n:
            self._klines.pop(0)


