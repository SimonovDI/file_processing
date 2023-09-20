import os
from pymongo.collection import Collection
from itertools import zip_longest
from base_class import BaseLoader
from connect_to_MongoDB import connect_to_base
from modules.file_reader.reader_json import ReaderJson
from modules.file_reader.reader_csv import ReaderCsv
from typing import Any, Mapping, Optional


class LoaderMongoDB(BaseLoader):
    """
    Load data to base MongoDB
    param:  file - name file
            name_db - DB name
            collection - collection name
    return: writes data to the database
    """

    @staticmethod
    def load(filename: str, name_db: str, collection: str, delimiter: str = ',') -> None:
        connect, client, name_collection = connect_to_base(name_db, collection)  # connect_to_MongoDB.connect_to_base
        if client is None:
            raise ValueError("Data is empty")
        data = LoaderMongoDB.read_with_determine_file_extension(filename, delimiter)
        if name_db in client.list_database_names() and collection in name_collection:  # check name_db in base
            LoaderMongoDB.update_data(data, connect)
        else:
            connect.insert_many(data)

    @staticmethod
    def update_data(data: list[dict[str, Any]], connect: Collection[Mapping[str, Any]]) -> None:
        """
        Update data in card in Mongo db collection
        param: list dictionary
        """

        if not data:
            raise ValueError("Data is empty")
        # aggregation query
        pipeline = [
            {"$project": {"_id": 0}}
        ]

        data_aggregate = connect.aggregate(pipeline)  # get data from document without '_id'
        count_keys_documents = connect.count_documents({})  # length dict in documents

        if len(data) >= count_keys_documents:
            for key_data, lst_data in zip_longest(data, data_aggregate):
                LoaderMongoDB.data_update_base(lst_data, connect, key_data)

        if len(data) < count_keys_documents:
            for key_data, lst_data in zip(data, data_aggregate):
                LoaderMongoDB.data_update_base(lst_data, connect, key_data)

    @staticmethod
    def data_update_base(filters: Mapping[str, Any], connect: Collection[Mapping[str, Any]],
                         key_json_data: Optional[dict]) -> None:

        """
       Check variable filters in collections

        """

        if isinstance(filters, dict):
            connect.update_one(filters, {'$set': key_json_data}, upsert=True)
        if filters is None:
            connect.insert_one(key_json_data)

    @staticmethod
    def read_with_determine_file_extension(filename: str, delimiter: str) -> list:
        mapping = {
            '.csv': ReaderCsv,
            '.json': ReaderJson
        }
        _, extension = os.path.splitext(filename)
        data = mapping[extension].read(filename, delimiter)  # type: ignore[arg-type]
        return data.data    # getting data from the reader, the date attribute in the dataclass


LoaderMongoDB.load('file.json', 'Mongo', 'test1')