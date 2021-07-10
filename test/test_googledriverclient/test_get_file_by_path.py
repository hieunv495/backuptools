import unittest
from os import path
from test.utils import SandboxTextCase

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestGetFileByPath(unittest.TestCase):

    client = GoogleDriverClient()

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_return_success(self):
        file = self.client.get_file_by_path('test/test-1/test-1.1')
        self.assertIsNotNone(file)
        self.assertEqual(file['name'], 'test-1.1')
