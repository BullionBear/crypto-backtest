from .order import *
from collections import deque


class Market:
    def __init__(self, timestamp, base, quote):
        self.trading_history = deque()
        self.kline_history = deque()

    def is_kline(self):
        if len(self.kline_history):
            return True
        return False

    def get_kline(self):
        pass

    def next_timestamp(self):
        pass

    def is_execute(self):
        if len(self.trading_history):
            return True
        return False

    def get_history(self):
        return self.trading_history.popleft()

    def send_limit(self, order: LimitOrder):
        pass

    def send_market(self, order: MarketOrder):
        pass
