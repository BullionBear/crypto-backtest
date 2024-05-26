from typing import Any

from .interface import IFeatureHandler
from collections import deque


class RollingWindowHandler(IFeatureHandler):
    def __init__(self, period):
        self.period = period
        self.q = deque(maxlen=self.period)

        self.running_sum = 0
        self.running_ss = 0

    def read(self, log_return: float):
        if len(self.q) == self.period:
            old_return = self.q.popleft()