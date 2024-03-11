import unittest
from backtest.components.core import ZipKLineIterator

class TestZipKLineIterator(unittest.TestCase):
    def test_iteration(self):
        # Example setup
        symbol = "BTCUSDT"
        start_time = 1678387200000  # Example start time
        end_time = 1678395600000  # Example end time
        source_dir = "/home/yite/crypto_data/binance/data"

        # Initialize the iterator
        kline_iterator = ZipKLineIterator(symbol, start_time, end_time, source_dir)

        # Expected data format (simplified example)
        expected_results = [
            {"open": 21013.32, "high": 21020.64, "close": 20854.93, "open_time": 1678388400000},
            {"open": 20856.3, "high": 20867.3, "close": 20116.66, "open_time": 1678392000000}
        ]

        # Iterate over the kline_iterator and compare each result with the expected output
        for expected, actual in zip(expected_results, kline_iterator):
            self.assertEqual(expected["open"], actual.open)
            self.assertEqual(expected["high"], actual.high)
            self.assertEqual(expected["close"], actual.close)
            self.assertEqual(expected["open_time"], actual.open_time)
            # Add other assertions as needed


if __name__ == '__main__':
    unittest.main()
