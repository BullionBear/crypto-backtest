import logging

from src.data.db import get_client
from datetime import datetime, timedelta
from binance.client import Client
import pytz

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    # Create a connection using MongoClient
    client = Client()
    res = client.get_ticker()
    # logging.info(res)
    res = sorted(res, key=lambda x: float(x['quoteVolume']), reverse=True)
    rank = 1
    not_interest = {"FDUSDUSDT", "USDCUSDT"}
    interest = []
    for i, r in enumerate(res):
        s = r['symbol']
        if s[-4:] != "USDT" or s in not_interest:
            continue
        v = r['quoteVolume']
        logging.info(f"{rank}, {s}: {v}")
        rank += 1
        interest.append(s)
        if rank > 75:
            break
    logging.info(interest)

