import pymongo

HOST = '172.17.0.3'
PORT = 27017


class MongoConfig:
    def __init__(self, host=HOST, port=PORT):
        self.client = pymongo.MongoClient(host, port)


def db_config(func):
    def wrapper(*args, **kwargs):
        mongo_config = MongoConfig()
        return func(mongo_config, *args, **kwargs)
    return wrapper
