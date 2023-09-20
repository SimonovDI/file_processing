import json
from modules.file_reader.base_class import BaseReader
from dataclasses import dataclass
from typing import Any
from datetime import datetime


@dataclass
class DataJson:
    data: Any
    headers: list
    created: datetime


class ReaderJson(BaseReader):
    """
    Reading data from json file
    """
    @staticmethod
    def read(filename: str, *args) -> DataJson:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
            data_json = json.loads(data)
        header = list(ReaderJson.get_headers(data_json))
        data = DataJson(data=data_json, headers=header, created=datetime.now())
        return data

    @staticmethod
    def get_headers(data_json):
        header = data_json[0].keys()
        return header
