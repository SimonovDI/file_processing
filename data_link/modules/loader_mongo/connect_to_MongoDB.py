import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Tuple, Any, Mapping


def connect_to_base(name_db: str, collection: str) -> Tuple[Collection[Mapping[str, Any]],
                                                            MongoClient[Mapping[str, Any]], list]:
    """
    Connect to base MongoDB
    param:  name_db - DataBase name
            collection - collection name
    return: What collection is the data being loaded into
    """
    load_dotenv()
    user = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASSWORD')
    name_database = os.getenv('MONGO_NAME_DATABASE')
    client: MongoClient = MongoClient(
        f'mongodb://{user}:{password}@localhost:27017/?authMechanism=DEFAULT&authSource={name_database}')
    db = client[name_db]  # DataBase name
    obj_collection = db[collection]  # collection name
    name_collection = db.list_collection_names()
    return obj_collection, client, name_collection,
