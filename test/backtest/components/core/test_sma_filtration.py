import unittest
import numpy as np
import pandas as pd
from backtest.components.core import SMAFiltration
from backtest.models import KLine


class TestSMAFiltration(unittest.TestCase):

    def setUp(self):
        # Setup a sample DataFrame
        self.sample_data = {
            "open_time": [1000, 2000, 3000],
            "open": [1.0, 2.0, 3.0],
            "high": [1.5, 2.5, 3.5],
            "low": [0.5, 1.5, 2.5],
            "close": [1.2, 2.2, 3.2],
            "volume": [100, 200, 300],
            "close_time": [1500, 2500, 3500],
            "quote_volume": [1000, 2000, 1500],
            "count": [10, 20, 15],
            "taker_buy_volume": [50, 100, 75],
            "taker_buy_quote_volume": [500, 1000, 800],
            "ignore": [0, 0, 0]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_sma_calculation(self):
        # Setup
        dummy_klines = [
            KLine(**{k: v[0] for k, v in self.sample_data.items()}),
            KLine(**{k: v[1] for k, v in self.sample_data.items()}),
            KLine(**{k: v[2] for k, v in self.sample_data.items()})
        ]
        sma_filter = SMAFiltration(n=2)

        # Act
        sma_filter.put(dummy_klines[0])
        res = sma_filter.get()
        self.assertTrue(np.isnan(res),f"sma is not np.nan: {res}")
        sma_filter.put(dummy_klines[1])
        res = sma_filter.get()
        self.assertAlmostEqual(res, 1.7)
        sma_filter.put(dummy_klines[2])
        res = sma_filter.get()
        self.assertAlmostEqual(res, 2.7)


if __name__ == '__main__':
    unittest.main()