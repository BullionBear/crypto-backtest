import unittest
import pandas as pd
from backtest.components.core import DataFrameKLineIterator
from backtest.models import KLine


class TestDataFrameKLineIterator(unittest.TestCase):
    def setUp(self):
        # Setup a sample DataFrame
        self.sample_data = {
            "open_time": [1000, 2000],
            "open": [1.0, 2.0],
            "high": [1.5, 2.5],
            "low": [0.5, 1.5],
            "close": [1.2, 2.2],
            "volume": [100, 200],
            "close_time": [1500, 2500],
            "quote_volume": [1000, 2000],
            "count": [10, 20],
            "taker_buy_volume": [50, 100],
            "taker_buy_quote_volume": [500, 1000],
            "ignore": [0, 0]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_iteration(self):
        # Initialize the iterator with the sample DataFrame
        iterator = DataFrameKLineIterator(self.df)

        # Manually create the expected KLine objects for comparison
        expected_klines = [
            KLine(**{k: v[0] for k, v in self.sample_data.items()}),
            KLine(**{k: v[1] for k, v in self.sample_data.items()})
        ]

        # Iterate over both the iterator and the expected KLine objects for comparison
        for expected, actual in zip(expected_klines, iterator):
            # Verify that each attribute matches
            self.assertEqual(expected.open, actual.open)
            self.assertEqual(expected.high, actual.high)
            self.assertEqual(expected.low, actual.low)
            self.assertEqual(expected.close, actual.close)
            self.assertEqual(expected.volume, actual.volume)
            self.assertEqual(expected.open_time, actual.open_time)
            self.assertEqual(expected.close_time, actual.close_time)
            self.assertEqual(expected.quote_volume, actual.quote_volume)
            self.assertEqual(expected.count, actual.count)
            self.assertEqual(expected.taker_buy_volume, actual.taker_buy_volume)
            self.assertEqual(expected.taker_buy_quote_volume, actual.taker_buy_quote_volume)
            self.assertEqual(expected.ignore, actual.ignore)


if __name__ == '__main__':
    unittest.main()
