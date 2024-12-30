from db.mongo_config import db_config


@db_config
def find_documents(mongo_config, db_name, collection_name, query):
    collection = mongo_config.client[db_name][collection_name]
    documents = collection.find(query)
    return list(documents)


@db_config
def find_all_documents(mongo_config, db_name, collection_name):
    collection = mongo_config.client[db_name][collection_name]
    documents = collection.find()
    return list(documents)
