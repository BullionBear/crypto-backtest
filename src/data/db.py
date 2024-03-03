from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoSingleton, cls).__new__(cls)
            mongo_url = 'mongodb://bullionbear:Sunshine4Jellybean@ec2-57-181-58-168.ap-northeast-1.compute.amazonaws.com:27017'
            cls._instance.client = MongoClient(mongo_url)
        return cls._instance.client


def get_client():
    return MongoSingleton()


def test_mongo_url(url):
    try:
        # Attempt to create a MongoClient object to test the connection
        client = MongoClient(url, serverSelectionTimeoutMS=5000) # 5 second timeout
        # Attempt to fetch the server info to check if connected
        client.admin.command('ping')
        print("MongoDB URL is available.")
        return True
    except ConnectionFailure:
        print("MongoDB URL is not available.")
        return False


if __name__ == '__main__':
    test_mongo_url(mongo_url)