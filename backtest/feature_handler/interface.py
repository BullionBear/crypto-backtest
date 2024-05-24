from abc import ABC, abstractmethod
from typing import Any


class IFeatureHandler(ABC):
    @abstractmethod
    def read(self, data: Any):
        """
        Handle input streaming
        """

    @abstractmethod
    def get(self):
        """
        Get current result
        """