import logging

from src.data import make_metadata
import tqdm

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT', 'SHIBUSDT', 'SOLUSDT', 'DOGEUSDT', 'PEPEUSDT', 'BNBUSDT', 'XRPUSDT', 'STRKUSDT',
              'WIFUSDT', 'ARBUSDT', 'ADAUSDT', 'BONKUSDT', 'OPUSDT', 'FETUSDT', 'UNIUSDT', 'LUNAUSDT', 'MATICUSDT',
              'WLDUSDT', 'FLOKIUSDT', 'AVAXUSDT', 'FILUSDT', 'NEARUSDT', 'DOTUSDT', 'ORDIUSDT', 'APTUSDT', 'RNDRUSDT',
              'LINKUSDT', 'LUNCUSDT', 'LTCUSDT', 'ETCUSDT', 'FTMUSDT', 'LSKUSDT', 'PIXELUSDT', 'MEMEUSDT', 'SUIUSDT',
              '1000SATSUSDT', 'AGIXUSDT', 'RUNEUSDT', 'ICPUSDT', 'MTLUSDT', 'INJUSDT', 'BCHUSDT', 'EURUSDT', 'SEIUSDT',
              'MANTAUSDT', 'DYDXUSDT', 'ENSUSDT', 'GALAUSDT', 'THETAUSDT']

    for symbol in symbols:
        make_metadata(symbol, '5s', '1h',
                      f'./data/processed/binance_{symbol}_metadata.json',
                      f'./data/processed/binance_{symbol}_metadata.json')
        logging.info(f"{symbol} finished!")