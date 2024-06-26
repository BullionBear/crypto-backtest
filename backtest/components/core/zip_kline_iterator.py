from backtest.virtual_components.core import KLineIterator
from backtest.models import KLine

import os
from datetime import datetime
from dateutil import rrule
import zipfile
import pandas as pd


class ZipKLineIterator(KLineIterator):
    def __init__(self, symbol, start_time, end_time, fs_path, granular='1h'):
        self.symbol = symbol
        self.start_time = start_time
        self.end_time = end_time
        self.fs_path = fs_path
        self.granular = granular
        self.fs = self._load_fs_list()

        self.current_zip_index = 0
        self.current_df_iter = iter([])  # Initialize an empty iterator

    def _load_fs_list(self):
        # This method should return a list of paths to the zip files to be processed
        # This is a placeholder for the logic to list relevant zip files based on the symbol and date range
        # Return a list of file paths
        symbol = self.symbol
        granular = self.granular
        start_date = datetime.utcfromtimestamp(self.start_time / 1000)
        end_date = datetime.utcfromtimestamp(self.end_time / 1000)  # Adjust end_date to include the end month
        return [os.path.join(self.fs_path, f'spot/monthly/klines/{symbol}/{granular}', f'{symbol}-{granular}-{dt.strftime("%Y-%m")}.zip')
                for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)]

    def __next__(self):
        try:
            return next(self.current_df_iter)
        except StopIteration:
            if self.current_zip_index < len(self.fs):
                zip_file = self.fs[self.current_zip_index]
                self.current_zip_index += 1
                self._process_zip_file(zip_file)
                return self.__next__()
            else:
                raise StopIteration

    def _process_zip_file(self, zip_file):
        with zipfile.ZipFile(zip_file, 'r') as z:
            csv_file = os.path.basename(zip_file).replace('.zip', '.csv')
            with z.open(str(csv_file)) as csv:
                df = pd.read_csv(csv, header=None,
                                 names=["open_time", "open", "high", "low", "close", "volume", "close_time",
                                        "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume",
                                        "ignore"])
        df = df[(df['open_time'] >= self.start_time) & (df['close_time'] < self.end_time)]
        self.current_df_iter = (KLine(**kline) for kline in df.to_dict('records'))


