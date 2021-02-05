# Main data model used in the pass to store and retrive information

#########################################################################################
# Library includes

import asyncio
import json
import pathlib
import os
from datetime import datetime

# Types
from typing import Any, Union
from pathlib import Path
#########################################################################################
# App includes

#########################################################################################

path_to_data: pathlib.Path = pathlib.Path('data/data.json')
date_format: str = "%d-%m-%y--%H:%M:%S"


class DataAcess:
    """
    Class that interfaces with files present on local machine and sychronises
    them with values stored in ram.
    """

    def __init__(self, *, filepath: Union[str, Path]) -> None:
        """
        Initiates a new instance of DataAccess class

        Args:
            filepath (Union[str, Path]): filepath to a file that will store data
        """
        pass

    pass


#########################################################################################
# Tests

# obj = Data()
# asyncio.get_event_loop().run_until_complete(
#     obj.update('', 'test', {"some_key": 1234}))

# print(obj.peek('test'))


#########################################################################################
# Old
class Data:
    """
    Data Model used in the application
    """

    def __init__(self):
        """
        Creates new data model
        """
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

    def peek(self, path_to_value: Any, *args) -> Any:
        path_to_value: str = str(path_to_value)
        splited = path_to_value.split('/')
        value = self._data

        for key in splited:
            if(not isinstance(value, dict)):
                break
            value = value.get(key, *args)
        return value

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

    async def update(self, root: Any, var_name: Any, new_value: Any):

        # Convert values to strings
        root: str = str(root)
        var_name: str = str(var_name)

        # Create pathfinder
        path = root.split('/')

        value = self._data
        for point in path:
            if(point == ''):
                break

            try:
                assert isinstance(value, (list, dict))
            except AssertionError:
                raise RuntimeError('Bad DataBase Entry')

            if isinstance(value, dict):
                value = value[point]
            elif isinstance(value, list):
                value = value[int(key)]

        try:
            assert isinstance(value, (list, dict))
        except AssertionError:
            raise RuntimeError('Bad DataBase Entry')

        if isinstance(value, dict):
            value[var_name] = new_value
        elif isinstance(value, list):
            value[int(var_name)] = new_value

        await self.save()
