from backtest.virtual_components.core import KLineIterator
from backtest.models import LimitOrder, MarketOrder, Trade, KLine

from typing import List
from collections import deque
import bisect


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
        self.current_kline: KLine = next(self.kline_iterator)
        self._ts = self.current_kline.close
        self.trading_history = deque()
        self.kline_history = deque()
        # Maintain the limit order execution
        self._ask: List[LimitOrder] = []
        self._bid: List[LimitOrder] = []
        # Market order
        self._market_order = []

    def get_ts(self):
        return self._ts

    def get_ask(self):
        return self._ask

    def get_bid(self):
        return self._bid

    def get_market(self):
        return self._market_order

    def next(self):
        for execution in self._execute():
            self.trading_history.append(execution)
        self.kline_history.append(self.current_kline)
        self.current_kline = next(self.kline_iterator)
        self._ts = self.current_kline.close

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
        if order.side in ['BUY', 'buy']:
            bisect.insort(self._ask, order, key=lambda o: o.price)  # sort in reverse order
        elif order.side in ['SELL', 'sell']:
            bisect.insort(self._bid, order, key=lambda o: -o.price)
        else:
            raise ValueError(f"order.side should be either BUY or SELL: {order.side=}")

    def send_market(self, order: MarketOrder):
        self._market_order.append(order)

    def cancel(self, order_id: str):
        for idx, order in enumerate(self._ask):
            if order.order_id == order_id:
                return self._ask.pop(idx)

        for idx, order in enumerate(self._bid):
            if order.order_id == order_id:
                return self._bid.pop(idx)
        raise ValueError(f"Cannot find {order_id=}")

    def _execute_buy_order(self):
        trades = []
        low = self.current_kline.low
        while self._ask and self._ask[-1].price >= low:
            order = self._ask.pop()
            trades.append(Trade(timestamp=self._ts,
                                base=order.base,
                                quote=order.quote,
                                side=order.side,
                                filled=order.amount,
                                order_id=order.order_id))
        return trades

    def _execute_sell_order(self):
        trades = []
        high = self.current_kline.high
        while self._bid and self._bid[-1].price <= high:
            order = self._bid.pop()
            trades.append(Trade(timestamp=self._ts,
                                base=order.base,
                                quote=order.quote,
                                side=order.side,
                                filled=order.amount,
                                order_id=order.order_id))
        return trades

    def _execute(self):
        return self._execute_buy_order() + self._execute_sell_order()
