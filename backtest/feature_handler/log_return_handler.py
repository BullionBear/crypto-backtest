from .interface import IFeatureHandler
import numpy as np


class LogReturnHandler(IFeatureHandler):
    def __init__(self):
        self.log_prices = []

    def read(self, price: float):
        if len(self.log_prices) == 2:
            self.log_prices.pop(0)
        self.log_prices.append(np.log(price))

    def get(self):
        if len(self.log_prices) != 2:
            return None
        return self.log_prices[-1] - self.log_prices[0]

    def is_valid(self):
        return len(self.log_prices) == 2
