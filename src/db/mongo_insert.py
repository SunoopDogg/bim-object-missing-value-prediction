from db.mongo_config import db_config


@db_config
def insert_json_to_collection(mongo_config, db_name, collection_name, json_data):
    mongo_config.client[db_name][collection_name].insert_many(json_data)
    print(f"Inserted data into collection: {collection_name}")
