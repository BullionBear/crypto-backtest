from backtest.virtual_components.core import KLineIterator
from backtest.models import KLine


class PostgresKlineIterator(KLineIterator):
    def __init__(self, connection):
        """
        Initializes the iterator with a DataFrame.

        :param df: DataFrame containing kline data.
        """
        self.conn = connection
        self.buf = self._create_iterator()

    def _create_iterator(self):
        """
        Creates an iterator from the DataFrame rows.

        :return: Iterator of KLine objects.
        """
        # Assuming the DataFrame structure matches the expected kline data format,
        # with columns ["open_time", "open", "high", "low", "close", "volume",
        # "close_time", "quote_volume", "count", "taker_buy_volume",
        # "taker_buy_quote_volume", "ignore"]
        return (KLine(**row) for index, row in self.df.iterrows())

    def __next__(self):
        """
        Return the next item from the iterator. If the iterator is exhausted,
        raise StopIteration.

        :return: Next KLine object from the DataFrame.
        """
        try:
            return next(self.current_df_iter)
        except StopIteration:
            raise StopIteration