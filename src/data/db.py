from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

mongo_url = 'mongodb://bullionbear:Sunshine4Jellybean@ec2-57-181-58-168.ap-northeast-1.compute.amazonaws.com:27017'


def get_client():  # Singleton
    return MongoClient(mongo_url)


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