from abc import ABC, abstractmethod


class KLineIterator(ABC):

    @abstractmethod
    def __next__(self):
        """Return the next item in the sequence. On reaching the end, raise StopIteration."""
        pass

    def __iter__(self):
        """Return the iterator object itself."""
        return self