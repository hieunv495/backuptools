import unittest
from os import path

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class SandboxTextCase(unittest.TestCase):

    root_path = 'test'
    base_container_name = 'sanbox-test-'
    client = GoogleDriverClient()
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
        self.client.rm_by_path_if_exist(self.container_path)
        self.container_file = self.client.create_folder_by_path(
            self.container_path)

    def tearDown(self):
        self.client.rm_by_path_if_exist(self.container_path)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')
