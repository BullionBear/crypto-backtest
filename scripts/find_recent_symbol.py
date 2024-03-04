from src.data.db import get_client
from datetime import datetime, timedelta
import pytz


if __name__ == '__main__':
    # Create a connection using MongoClient
    client = get_client()

    # Access your database
    db = client.get_database('binance')

    # Access your collection
    collection = db.get_collection('wsMarketStatEvents')
    # Ensure that now and five_minutes_ago are in UTC
    utc_zone = pytz.utc
    now = datetime.now(utc_zone)
    five_minutes_ago = now - timedelta(minutes=5)
    query = {'E': {'$gt': five_minutes_ago, '$lt': now}}
    print(query)

    # Find all unique values in the field 's'
    unique_values = collection.distinct('s', query)

    # Print the list of unique values
    print(list(filter(lambda s: s[-4:] == 'USDT', unique_values)))