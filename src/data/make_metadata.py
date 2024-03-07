import logging
import os.path
from typing import List, Tuple
from src.data.db import get_client
from tqdm import tqdm
from datetime import datetime, timedelta, timezone
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
    collection = db.get_collection('wsMarketStatEvents')
    projection = {"E": 1}
    logging.info(f'Make metadata parameter {within_interval=}, {minimal_range=}')
    # Initialize first document
    if reference and os.path.exists(reference):
        logging.info(f'Read cache {reference}')
        with open(reference, 'r') as jfile:
            cache = json.load(jfile)
        intervals = [[datetime.fromisoformat(interval["left"]), datetime.fromisoformat(interval["right"])]
                     for interval in cache["intervals"]]
        within_interval = cache["metadata"]["within_interval"]
        minimal_range = cache["metadata"]["minimal_range"]
        # make sure the first result interval overlap to last
        start_time = (datetime.fromisoformat(cache["metadata"]["end_time"]) -
                      convert_to_timedelta(minimal_range))
        logging.info(f'Cache parameter {within_interval=}, {minimal_range=}')
    else:
        logging.info(f'Cannot find  {within_interval=}, {minimal_range=}')
        intervals = []
        start_time = next(collection.find({'s': symbol}, projection).sort({'E': 1}).limit(1))['E']
    end_time = list(collection.find({'s': symbol}, projection).sort({'E': -1}).limit(1))[0]['E']  # Don't use now, it meets time zone issue
    within_delta = convert_to_timedelta(within_interval)
    minimal_delta = convert_to_timedelta(minimal_range)
    adj_intervals = find_continuous_intervals(within_delta, start_time, end_time, symbol)
    if intervals:
        intervals[-1][1] = adj_intervals[0][1]
        intervals += adj_intervals[1:]
    else:
        intervals += adj_intervals
    intervals = list(filter(lambda x: (x[1] - x[0]) > minimal_delta, intervals))

    logging.info(f"Number of interval: {len(intervals)}")

    with open(dst, 'w') as jfile:
        json.dump({
            "metadata": {
                "symbol": symbol,
                "within_interval": within_interval,
                "minimal_range": minimal_range,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            },
            "intervals": [
                {
                    "left": interval[0].isoformat(),
                    "right": interval[1].isoformat(),
                    "ref": ""
                }
                for interval in intervals
            ]
        }, jfile, indent=4)
    return 0

def make_dataset_with_cache(symbol: str, reference: str = '', dst: str = ''):
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
    collection = db.get_collection('wsMarketStatEvents')
    projection = {"E": 1}
    if reference and os.path.exists(reference):
        logging.info(f'Read cache {reference}')
        with open(reference, 'r') as jfile:
            cache = json.load(jfile)
        intervals = [[datetime.fromisoformat(interval["left"]), datetime.fromisoformat(interval["right"])]
                     for interval in cache["intervals"]]
        within_interval = cache["metadata"]["within_interval"]
        minimal_range = cache["metadata"]["minimal_range"]
        # make sure the first result interval overlap to last
        start_time = (datetime.fromisoformat(cache["metadata"]["end_time"]) -
                      convert_to_timedelta(minimal_range))
        logging.info(f'Cache parameter {within_interval=}, {minimal_range=}')
    else:
        logging.error(f"Unable to find cache reference {reference}")
        return
    within_delta = convert_to_timedelta(within_interval)
    minimal_delta = convert_to_timedelta(minimal_range)
    end_time = list(collection.find({'s': symbol}, projection).sort({'E': -1}).limit(1))[0]['E']  # Don't use now, it meets time zone issue
    find_continuous_intervals(within_delta, start_time, end_time, symbol)
    adj_intervals = find_continuous_intervals(within_delta, start_time, end_time, symbol)

def dt_iterator(start: datetime, end: datetime, symbol: str):
    # Setup DB
    client = get_client()
    db = client.get_database('binance')
    collection = db.get_collection('wsMarketStatEvents')
    projection = {"E": 1}
    current_time_doc = next(collection.find({'s': symbol, 'E': {'$gte': start}}, projection).sort("E", 1).limit(1),
                            None)
    if not current_time_doc:
        return  # No data found, exit the iterator
    current_time = current_time_doc['E']
    step = convert_to_timedelta('3h')
    step_p = (end - start) / step  # Calculate total number of steps
    # Initialize tqdm with the total number of steps, converting to integer
    pbar = tqdm(total=int(step_p))
    while end - current_time > timedelta(seconds=0):  # current_time < end doesn't work cz of tz
        subsequent = current_time + step
        for doc in collection.find({'s': symbol, 'E': {'$gte': current_time, '$lt': min(subsequent, end)}}):
            yield doc['E']
        current_time = subsequent
        pbar.update(1)
    pbar.close()
    return


def find_continuous_intervals(threshold, first, last, symbol):
    # Initialize the list to store the intervals
    intervals = []
    # Start the first interval with the first value
    start = first
    end = start
    prev = start  # Keep track of the previous element for comparison

    for current in dt_iterator(first, last, symbol):
        # Check if the current and previous elements are continuous
        if current - prev < threshold:
            end = current  # Update the end of the current interval
        else:
            # If not continuous, add the current interval and start a new one
            intervals.append([start, end])
            start = current
            end = current
        prev = current  # Update the previous element for the next iteration
    # After the loop, add the last interval if not already added
    if not intervals or intervals[-1][1] != end:
        intervals.append([start, end])

    return intervals


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
    # make_metadata("BTCUSDT", '5s', '1h', '',
    #               './data/processed/binance_acmusdt_metadata.json')
    symbol = 'ETHUSDT'
    make_metadata(symbol, '5s', '1h', f'./data/processed/binance_{symbol}_metadata.json',
                  f'./data/processed/binance_{symbol}_metadata.json')