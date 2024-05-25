from typing import Any

from .interface import IFeatureHandler


class MergeHandler(IFeatureHandler):
    """
    Merge 1s Kline into 30s/1m/... KLine
    """
    def __init__(self, period):
        self.period = period
        self.buf = []

    def read(self, data: Any):
        if len(self.buf) == self.period:
            self.buf.clear()
        self.buf.append(data)

    def get(self):
        if len(self.buf) != self.period:
            return None
        return

    def _summary(self):
        # Not implement
        return

