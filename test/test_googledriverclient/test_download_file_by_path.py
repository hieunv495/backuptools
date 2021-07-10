import unittest
from os import path
from test.utils import SandboxTextCase

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestDownloadFileByPath(unittest.TestCase):

    client = GoogleDriverClient()

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_with_default_name(self):
        driver_path = 'test/test-1/test-1.1/test-1.1.1.txt'
        file = self.client.get_file_by_path(driver_path)

        self.assertIsNotNone(file)

        local_file_path = self.client.download_file_by_path(
            driver_path, local_folder_path='./')

        self.assertIsNotNone(local_file_path)
        self.assertTrue(path.isabs(local_file_path))
        self.assertTrue(path.isfile(local_file_path))
        self.assertEqual(path.basename(local_file_path), file['name'])

    def test_with_custom_name(self):
        driver_path = 'test/test-1/test-1.1/test-1.1.1.txt'
        file = self.client.get_file_by_path(driver_path)

        self.assertIsNotNone(file)

        custom_name = 'test-custom-name.txt'

        local_file_path = self.client.download_file_by_path(
            driver_path, local_folder_path='./', local_file_name=custom_name)

        self.assertIsNotNone(local_file_path)
        self.assertTrue(path.isabs(local_file_path))
        self.assertTrue(path.isfile(local_file_path))
        self.assertEqual(path.basename(local_file_path), custom_name)
