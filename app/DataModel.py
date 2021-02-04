# Main data model used in the pass to store and retrive information

#########################################################################################
# Library includes

import asyncio
import json
import pathlib
import os
from datetime import datetime
from typing import Any
#########################################################################################
# App includes

#########################################################################################

path_to_data: pathlib.Path = pathlib.Path('data/data.json')
date_format: str = "%d-%m-%y--%H:%M:%S"


class Data:

    def __init__(self):

        # Lock that will be used in async functions
        self.lock = asyncio.Lock()
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

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

    # Main fuction to dump data to file
    def _dump(self) -> None:
        now_time = datetime.now().strftime(date_format)
        tmp_file_name: str = f'{now_time}.tmp.json'
        tmp_file_path: str = f'data/{tmp_file_name}'

        with open(tmp_file_path, 'wt') as f:
            json.dump(self._data, f, indent=4)

        os.replace(tmp_file_path, path_to_data)

    # Main function to load data from file
    def _load(self) -> None:
        try:
            with open(path_to_data, 'rt') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data: dict = {}

    def get(self, key: Any, *args) -> Any:
        """
        Gets specified key from data 

        Args:
            key (Any): key to be accesed

        Returns:
            Any: Returns value from a given key
        """
        return self._data.get(str(key), *args)

    #########################################################################################
    # Async stuff

    async def save(self):
        """
        Saves data to a file
        """
        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

    async def load(self):
        """
        Loads data form a file
        """
        async with self.lock:
            await self.loop.run_in_executor(None, self._load)

    async def put(self, key: Any, value: Any):
        """
        Edits entry at specified key

        Args:
            key (Any): specified key
            value (Any): value to be set
        """
        self._data[str(key)] = value
        await self.save()
