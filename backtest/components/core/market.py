from backtest.virtual_components.core import KLineIterator
from collections import deque


class KLineMarket:
    """
    A KLineMarket maintain three components
    - timestamp: the latest time of the market
    - iterator: container for market requesting the market data before timestamp
    - orders: orders react to the market
    For a backtest, user can operate
    - next(): Go to next status of the market
    - get_timestamp(): Get current timestamp of a Market
    - send(order: Order) -> str: Send an order to the market and get its order_id
    - cancel(order_id: str): Cancel the order through order_id
    - is_kline() -> bool: Check if the there any updated information
    - get_kline() -> KLine: Get latest kline information
    - is_execution() -> bool: Check if there is any executed order
    - get_execution() -> Execution: Get the latest execution
    """
    def __init__(self, kline_iterator: KLineIterator):
        self.kline_iterator = kline_iterator
        self.current_kline = next(self.kline_iterator)
        self.ts = self.current_kline.open
        self.trading_history = deque()
        self.kline_history = deque()
        # Maintain the limit order execution
        self.limit_buy_order = {}
        self.limit_sell_order = {}

    def get_ts(self):
        return self.ts

    def next(self):
        execution = self._execute()
        pass

    def is_kline(self):
        if len(self.kline_history):
            return True
        return False

    def get_kline(self):
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
