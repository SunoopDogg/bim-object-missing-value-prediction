import pymongo

HOST = '172.17.0.3'
PORT = 27017
DB_NAME = 'bim'


class MongoConfig:
    def __init__(self, host=HOST, port=PORT, db_name=DB_NAME):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db_name]
        print(f"Connected to database: {db_name}")
