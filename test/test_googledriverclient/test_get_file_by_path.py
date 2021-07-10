import os
import unittest
from test import ROOT_ID
from test.utils import SandboxTextCase

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestGetFileByPath(unittest.TestCase):

    client = GoogleDriverClient(root_id=ROOT_ID)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_return_success(self):
        path = 'TestGetFileByPath_container/middle/child'
        file1 = self.client.get_or_create_folder_by_path(path)
        self.assertIsNotNone(file1)
        file2 = self.client.get_file_by_path(path)
        self.assertIsNotNone(file2)
        self.assertEqual(file2['name'], os.path.basename(path))

        self.client.rm_by_path_if_exist('TestGetFileByPath_container')

    def test_with_error(self):
        file = self.client.get_file_by_path('unknown_path')
        self.assertIsNone(file)
