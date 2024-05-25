from typing import Any

from .interface import IFeatureHandler
from collections import deque


class ShiftHandler(IFeatureHandler):
    def __init__(self, n_shift):
        self.n_shift = n_shift
        self.q = deque(maxlen=self.n_shift)

    def read(self, data: Any):
        if len(self.q) == self.n_shift:
            self.q.popleft()
        self.q.append(data)

    def get(self):
        if len(self.q) != self.n_shift:
            return None
        return self.q[0]

    def is_valid(self):
        return len(self.q) == self.n_shift
