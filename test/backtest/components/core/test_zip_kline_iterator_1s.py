import unittest
from backtest.components.core import ZipKLineIterator1s


class TestZipKLineIterator(unittest.TestCase):

    def setUp(self):
        # Example setup
        symbol = "BTCUSDT"
        start_time = 1675209600000  # Example start time
        end_time = 1676332800000  # Example end time
        source_dir = "/home/yite/crypto_data/binance/data"

        # Initialize the iterator
        self.kline_iterator = ZipKLineIterator1s(symbol, start_time, end_time, source_dir)

    def test_iteration(self):
        # Expected data format (simplified example)
        expected_results = [
            {"open": 23125.13, "high": 23127.73, "close": 23126.4, "open_time": 1675209600000},
            {"open": 23127.02, "high": 23127.23, "close": 23126.38, "open_time": 1675209601000}
        ]

        # Iterate over the kline_iterator and compare each result with the expected output
        for expected, actual in zip(expected_results, self.kline_iterator):
            self.assertEqual(expected["open"], actual.open)
            self.assertEqual(expected["high"], actual.high)
            self.assertEqual(expected["close"], actual.close)
            self.assertEqual(expected["open_time"], actual.open_time)