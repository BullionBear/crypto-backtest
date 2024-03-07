import logging

from src.data.db import get_client
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    interest = ['BTCUSDT', 'ETHUSDT', 'SHIBUSDT', 'SOLUSDT', 'PEPEUSDT', 'DOGEUSDT', 'BNBUSDT', 'XRPUSDT', 'NEARUSDT',
                'FETUSDT', 'RNDRUSDT', 'WIFUSDT', 'STRKUSDT', 'ARBUSDT', 'WLDUSDT', 'BONKUSDT', 'UNIUSDT', 'FLOKIUSDT',
                'AGIXUSDT', 'OPUSDT', 'MATICUSDT', 'FILUSDT', 'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'ORDIUSDT', 'SUIUSDT',
                'LUNAUSDT', 'FTMUSDT', 'APTUSDT', 'PIXELUSDT', 'AIUSDT', 'MTLUSDT', 'ARKMUSDT', 'LINKUSDT', 'ATOMUSDT',
                'LUNCUSDT', 'MEMEUSDT', 'ETCUSDT', 'ICPUSDT', '1000SATSUSDT', 'RUNEUSDT', 'MANTAUSDT', 'LTCUSDT',
                'SEIUSDT', 'ARUSDT', 'RSRUSDT', 'INJUSDT', 'DYDXUSDT', 'VANRYUSDT', 'EURUSDT', 'GALAUSDT', 'BCHUSDT',
                'GRTUSDT', 'THETAUSDT', 'PHBUSDT', 'NFPUSDT', 'AAVEUSDT', 'XAIUSDT', 'TIAUSDT', 'CRVUSDT', 'ZILUSDT',
                'JUPUSDT', 'HBARUSDT', 'ENSUSDT', 'SANDUSDT', 'OCEANUSDT', 'TRXUSDT', 'SUSHIUSDT', 'PEOPLEUSDT',
                'ALTUSDT', 'JASMYUSDT', 'FISUSDT', 'FTTUSDT', 'STXUSDT']

    client = get_client()
    db = client.get_database('binance')
    collection = db.get_collection('wsMarketStatEvents')
    # Deleting documents where the 's' field's value is not in the interest list
    result = collection.delete_many({'s': {'$nin': interest}})

    logging.info(f"Deleted finished!")
    end_time = next(collection.find({'s': 'BTCUSDT'}).sort({'E': -1}).limit(1))['E']
    start_time = end_time - timedelta(seconds=10)
    query = {'E': {'$gt': start_time, "$lt": end_time}}
    symbols = [s for s in collection.distinct('s', query)]
    logging.info(f"{symbols=}")

