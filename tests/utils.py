import os
import unittest
from contextlib import contextmanager
from os import path
from typing import Generator, Iterator, Optional

from src.googledriveclient import GoogleDriveClient
from src.type import (FileExistedException, FileMeta, FileNotFoundException,
                      ParentNotFoundException)

from tests import CREDENTIALS_PATH, ROOT_ID


class SandboxTextCase(unittest.TestCase):

    root_path = 'sanbox'
    base_container_name = 'sanbox-test-'
    client = GoogleDriveClient(root_id=ROOT_ID)
    count = 0

    container_file: FileMeta = None

    @property
    def container_path(self):
        return self.__class__.root_path + '/' + self.container_name

    @property
    def container_name(self):
        return self.__class__.base_container_name + str(self.__class__.count)

    def setUp(self):
        self.__class__.count += 1
        # print('Setup')
        self.client.rm_by_path_if_exist(self.container_path)
        self.container_file = self.client.get_or_create_folder_by_path(
            self.container_path)

    def tearDown(self):
        self.client.rm_by_path_if_exist(self.container_path)

    def __init__(self, methodName):
        super().__init__(methodName)
        if not self.client.is_connected:
            self.client.connect(CREDENTIALS_PATH)


class FileTools():

    @classmethod
    def create_file(cls, file_path: str, file_size: int):
        with open(file_path, 'wb') as f:
            f.write(os.urandom(file_size))


class TmpFile():

    def __init__(self, file_name: str, file_size: int, parent_path: str = './tmp-files'):
        self.file_name = file_name
        self.file_size = file_size
        self.parent_path = parent_path

        self.file_path = os.path.abspath(
            os.path.join(self.parent_path, self.file_name))

        os.makedirs(self.parent_path, exist_ok=True)

        FileTools.create_file(self.file_path, self.file_size)

    def __enter__(self):
        return self.file_path

    def __exit__(self,  exc_type, exc_value, exc_traceback):
        os.remove(self.file_path)
