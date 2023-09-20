import pandas as pd
from dataclasses import dataclass
from modules.file_reader.base_class import BaseReader
from typing import Any
from datetime import datetime
from modules.file_reader.reader_json import ReaderJson


@dataclass
class DataCsv:
    data: Any
    headers: list
    created: datetime


class ReaderCsv(BaseReader):

    @staticmethod
    def read(filename: str, delimiter: str) -> DataCsv:
        """
        param:  file - csv filename,
                delimiter - line separator,
        return: list[dict{str, str}]
        """

        data = pd.read_csv(filename, sep=delimiter).dropna()
        return_data = data.to_dict(orient='records')
        header = list(ReaderJson.get_headers(return_data))
        data = DataCsv(data=return_data, headers=header, created=datetime.now())
        return data


