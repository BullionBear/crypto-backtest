import logging
import os
import json
from datetime import datetime
from src.data import make_binance_market_stat

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    for root, dirs, files in os.walk('./data/processed/'):
        for f in files:
            path = os.path.join(root, f)
            with open(path, 'r') as jfile:
                metadata = json.load(jfile)
            symbol = metadata['metadata']['symbol']
            for i, interval in enumerate(metadata['intervals']):
                start_time = datetime.fromisoformat(interval['left'])
                end_time = datetime.fromisoformat(interval['right'])
                dst = f'./data/raw/binance_{symbol}_{i}.csv'
                logging.info(f'{start_time=}, {end_time=}')

    # json.dumps()