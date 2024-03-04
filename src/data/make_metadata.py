import logging

from src.data.db import get_client
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def make_metadata(symbol: str, within_interval: str, minimal_range: str, reference: str = '', dst: str = '') -> int:
    """
    :param symbol: trading pairs, like BTCUSDT, ETHBTC
    :param within_interval: acceptable interval between records
    :param minimal_range: acceptable contiguous data range
    :param reference: cache date path, empty string means no cache references
    :param dst: storage path, can be the same to reference
    :return: status
    """
    client = get_client()
    db = client.get_database('binance')
    collection = db.get_collection('testMarketStatEvents')
    # Initialize first document
    if reference:
        doc = collection.find({'s': symbol}).limit(1)
        current = list(doc)[0]
        start_time = current['E']
    else:
        doc = collection.find({'s': symbol}).limit(1)
        current = list(doc)[0]
        start_time = current['E']
    # Set stopped condition
    doc = collection.find({'s': symbol}).limit(-1)
    end_time = list(doc)[0]['E']

    # Set looping step and cache
    step = convert_to_timedelta('10m')
    left = start_time
    right = start_time
    # Result
    res = []
    # Filter parameters
    within_interval = convert_to_timedelta(within_interval)
    minimal_range = convert_to_timedelta(minimal_range)
    while start_time < end_time:
        next_time = start_time + step
        for doc in collection.find({'s': symbol, 'E': {'$gt': start_time, '$lt': next_time}}):
            if doc['L'] == current['L']:
                continue
            if doc['E'] - current['E'] < within_interval:
                right = doc['E']
            else:
                if right - left > minimal_range:
                    res.append([left, right])
                left = doc['E']
                right = doc['E']
            current = doc
        start_time = next_time
    logging.info(f"Result = {res}")
    return 0


def convert_to_timedelta(duration_shorthand: str):
    # Extract the number and the unit from the string
    num = int(''.join(filter(str.isdigit, duration_shorthand)))
    unit = ''.join(filter(str.isalpha, duration_shorthand))

    # Convert to timedelta based on the unit
    if unit == 's':
        return timedelta(seconds=num)
    elif unit == 'm':
        return timedelta(minutes=num)
    elif unit == 'h':
        return timedelta(hours=num)
    elif unit == 'd':
        return timedelta(days=num)
    else:
        raise ValueError("Unsupported time unit in string")


if __name__ == '__main__':
    make_metadata("BTCUSDT", '5s', '1h', '',
                  './data/processed/binance_acmusdt_metadata.json')