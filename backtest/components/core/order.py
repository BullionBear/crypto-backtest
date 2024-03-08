from uuid import uuid4


class Order:
    def __init__(self, base: str, quote: str, side: str, amount: float):
        self._order_id = uuid4()
        self.base = base
        self.quote = quote
        self.side = side
        self.amount = amount  # base amount

    @property
    def order_id(self):
        return self._order_id


class LimitOrder(Order):
    def __init__(self, base: str, quote: str, side: str, amount: float, price: float):
        super().__init__(base, quote, side, amount)
        self.price = price


class MarketOrder(Order):
    def __init__(self, base: str, quote: str, side: str, amount: float):
        super().__init__(base, quote, side, amount)


class StopLimitOrder(Order):
    def __init__(self, base: str, quote: str, side: str, amount: float, stop_price: float, limit_price: float):
        super().__init__(base, quote, side, amount)
        self.stop_price = stop_price
        self.limit_price = limit_price





