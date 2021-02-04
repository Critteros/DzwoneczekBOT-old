# Main data model used in the pass to store and retrive information

#########################################################################################
# Library includes

import asyncio
import json
import pathlib
import os
from datetime import datetime
#########################################################################################
# App includes

#########################################################################################

path_to_data: pathlib.Path = pathlib.Path('data/data.json')
date_format: str = "%d-%m-%y--%H:%M:%S"


class Data:

    def __init__(self):

        # Lock that will be used in async functions
        self.lock = asyncio.Lock()

        # Check if dir exist
        try:
            os.mkdir('data')
        except OSError:
            pass

        # Intial load of data
        try:
            with open(path_to_data, "rt") as f:
                self._data: dict = json.load(f)
        except (OSError, json.JSONDecodeError, FileNotFoundError):
            self._data: dict = {}

        #self._data = {"alan": "sadasdasd", "sadasd": True}

    #########################################################################################

    def _dump(self) -> None:
        now_time = datetime.now().strftime(date_format)
        tmp_file_name: str = f'{now_time}.tmp.json'
        tmp_file_path: str = f'data/{tmp_file_name}'

        with open(tmp_file_path, 'wt') as f:
            json.dump(self._data, f, indent=4)

        os.replace(tmp_file_path, path_to_data)

    #########################################################################################
    # Async stuff

    async def save(self):
        pass


Data()._dump()
