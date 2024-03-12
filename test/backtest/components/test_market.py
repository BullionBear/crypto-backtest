import unittest
import pandas as pd
from backtest.components.core import DataFrameKLineIterator
from backtest.components import KLineMarket
from backtest.models import MarketOrder, LimitOrder
from backtest.models import KLine


class TestKLineMarket(unittest.TestCase):
    def setUp(self):
        # Setup a sample DataFrame
        sample_data = {
            "open_time": [1000, 2000],
            "open": [1.0, 2.0],
            "high": [1.5, 2.5],
            "low": [0.5, 1.5],
            "close": [1.2, 2.2],
            "volume": [100, 200],
            "close_time": [1999, 2999],
            "quote_volume": [1000, 2000],
            "count": [10, 20],
            "taker_buy_volume": [50, 100],
            "taker_buy_quote_volume": [500, 1000],
            "ignore": [0, 0]
        }
        df = pd.DataFrame(sample_data)
        self.kline_iterator = DataFrameKLineIterator(df)

    def test_next(self):
        market = KLineMarket(self.kline_iterator)
        self.assertEqual(market.next(), True)
        self.assertEqual(market.next(), False)

    def test_send_market(self):
        market = KLineMarket(self.kline_iterator)
        market.send_market(MarketOrder(
            timestamp=1000,
            base="TEST",
            quote="USDT",
            side="BUY",
            amount=10,
        ))
        market.next()
        self.assertEqual(market.is_trade(), True)
        trade = market.get_trade()
        self.assertEqual(trade.side, 'BUY')
        self.assertEqual(trade.filled, 10.0)
        market.send_market(MarketOrder(
            timestamp=1000,
            base="TEST",
            quote="USDT",
            side="SELL",
            amount=15,
        ))
        market.next()
        self.assertEqual(market.is_trade(), True)
        trade = market.get_trade()
        self.assertEqual(trade.side, 'SELL')
        self.assertEqual(trade.filled, 15.0)


