import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MongoSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoSingleton, cls).__new__(cls)
            # Primary and fallback connection URLs
            first_url = 'mongodb://bullionbear:Sunshine4Jellybean@localhost:27017'
            fallback_url = 'mongodb://bullionbear:Sunshine4Jellybean@ec2-57-181-58-168.ap-northeast-1.compute.amazonaws.com:27017'
            try:
                # Set serverSelectionTimeoutMS to 1000 for 1-second timeout
                cls._instance.client = MongoClient(first_url, serverSelectionTimeoutMS=1000)
                # Attempt a quick operation to check the connection
                cls._instance.client.admin.command('ping')
                logging.info(f"Connected to MongoDB using primary URL: {first_url}")
            except ConnectionFailure:
                try:
                    # Attempt to connect to the fallback URL with 1-second timeout
                    cls._instance.client = MongoClient(fallback_url, serverSelectionTimeoutMS=1000)
                    # A quick operation to check the connection
                    cls._instance.client.admin.command('ping')
                    logging.info(f"Primary URL failed, connected to MongoDB using fallback URL: {fallback_url}")
                except ConnectionFailure:
                    logging.error("Both primary and fallback MongoDB connections failed.")
        return cls._instance.client

def get_client():
    return MongoSingleton()


def test_mongo_url(url):
    try:
        # Attempt to create a MongoClient object to test the connection
        client = MongoClient(url, serverSelectionTimeoutMS=1000)  # 1 second timeout
        # Attempt to fetch the server info to check if connected
        client.admin.command('ping')
        logging.info("MongoDB URL is available.")
        return True
    except ConnectionFailure:
        logging.error("MongoDB URL is not available.")
        return False


if __name__ == '__main__':
    test_mongo_url("mongodb://bullionbear:Sunshine4Jellybean@ec2-57-181-58-168.ap-northeast-1.compute.amazonaws.com:27017")