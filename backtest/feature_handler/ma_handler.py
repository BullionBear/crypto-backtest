from typing import Union
from .interface import IFeatureHandler
import queue


class MovingAverageHandler(IFeatureHandler):
    """
    Moving average of log returns, log return is defined by
    log P_t - log P_{t-1}, the input should be log return directly
    """
    def __init__(self, period: int, rescale: float):
        self.period = period
        self.rescale = rescale  # The parameter is to rescale the result for annualized return or other scale
        self.q = queue.Queue(maxsize=period)
        self.running_sum = 0

    def read(self, log_return: float):
        if self.q.qsize() >= self.period:
            old_return = self.q.get()
            self.running_sum -= old_return
        self.q.put(log_return)
        self.running_sum += log_return

    def get(self) -> Union[float, None]:
        if self.q.qsize() != self.period:
            return None
        return self.running_sum / self.period * self.rescale

    def is_valid(self):
        return self.q.qsize() == self.period
