from db.mongo_config import MongoConfig

mongo_config = MongoConfig()


def show_collections():
    collections = mongo_config.db.list_collection_names()
    print(collections)


def insert_json_to_collection(collection_name, json_data):
    collection = mongo_config.db[collection_name]
    collection.insert_many(json_data)
    print(f"Inserted data into collection: {collection_name}")
