import unittest
from backtest.components.core import ZipKLineIterator


class TestZipKLineIterator(unittest.TestCase):

    def setUp(self):
        # Example setup
        symbol = "BTCUSDT"
        start_time = 1678387200000  # Example start time
        end_time = 1678395600000  # Example end time
        source_dir = "/home/yite/crypto_data/binance/data"

        # Initialize the iterator
        self.kline_iterator = ZipKLineIterator(symbol, start_time, end_time, source_dir)

    def test_iteration(self):
        # Expected data format (simplified example)
        expected_results = [
            {"open": 21013.32, "high": 21020.64, "close": 20854.93, "open_time": 1678388400000},
            {"open": 20856.3, "high": 20867.3, "close": 20116.66, "open_time": 1678392000000}
        ]

        # Iterate over the kline_iterator and compare each result with the expected output
        for expected, actual in zip(expected_results, self.kline_iterator):
            self.assertEqual(expected["open"], actual.open)
            self.assertEqual(expected["high"], actual.high)
            self.assertEqual(expected["close"], actual.close)
            self.assertEqual(expected["open_time"], actual.open_time)
            # Add other assertions as needed

    def test_to_dataframe(self):
        # Expected data format (simplified example)
        expected_results = [
            {"open": 21013.32, "high": 21020.64, "close": 20854.93, "open_time": 1678388400000},
            {"open": 20856.3, "high": 20867.3, "close": 20116.66, "open_time": 1678392000000}
        ]

        klines = self.kline_iterator.to_dataframe()
        for idx, kline in klines.iterrows():
            expected = expected_results[idx]
            self.assertAlmostEqual(expected["open"], kline.open)
            self.assertAlmostEqual(expected["high"], kline.high)
            self.assertAlmostEqual(expected["close"], kline.close)
            self.assertAlmostEqual(expected["open_time"], kline.open_time)


if __name__ == '__main__':
    unittest.main()
