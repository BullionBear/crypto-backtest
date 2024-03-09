import unittest
import pandas as pd
from backtest.ffn.portfolio import (
    calc_return, calc_interval_return, calc_interval_volatility,
    calc_mdd, calc_interval_sharpe_ratio, convert_to_milliseconds
)


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        data = {
            'time': [1600000000000 + 86400_000 * i for i in range(7)],
            'nav': [1, 1.1, 1.2, 1.3, 1.1, 0.9, 0.8]
        }
        self.df = pd.DataFrame(data)

    def test_calc_return(self):
        result = calc_return(self.df, 'nav')

        self.assertAlmostEqual(result, (0.8 - 1) / 1)

    def test_calc_interval_return(self):
        interval = '1d'
        result = calc_interval_return(self.df, 'time', 'nav', interval)
        self.assertAlmostEqual(result, (0.8 - 1) / 6)

    def test_calc_interval_volatility(self):
        interval = '1d'
        result = calc_interval_volatility(self.df, 'time', 'nav', interval)
        self.assertTrue(isinstance(result, float))  # Consider refining this test for more accuracy

    def test_calc_mdd(self):
        result = calc_mdd(self.df, 'nav')
        self.assertAlmostEqual(result, (1.3 - 0.8) / 1.3)

    def test_calc_interval_sharpe_ratio(self):
        interval = '1d'
        result = calc_interval_sharpe_ratio(self.df, 'time', 'nav', interval)
        self.assertTrue(isinstance(result, float))  # Add more detailed tests based on Sharpe Ratio calculation

    def test_convert_to_milliseconds(self):
        self.assertEqual(convert_to_milliseconds('1s'), 1000)
        self.assertEqual(convert_to_milliseconds('1m'), 60000)
        self.assertEqual(convert_to_milliseconds('1h'), 3600000)
        self.assertEqual(convert_to_milliseconds('1d'), 86400000)

if __name__ == '__main__':
    unittest.main()