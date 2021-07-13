import unittest

from src.googledriveclient import GoogleDriveClient
from tests import CREDENTIALS_PATH, ROOT_ID


class TestGetFileById(unittest.TestCase):

    client = GoogleDriveClient(root_id=ROOT_ID)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect(CREDENTIALS_PATH)

    def test_return_success(self):
        file_name = 'TestGetFileById_test_return_success'
        file1 = self.client.get_or_create_folder_by_path(file_name)
        self.assertIsNotNone(file1)

        file2 = self.client.get_file_by_id(file1['id'])
        self.assertIsNotNone(file2)
        self.assertEqual(file2['name'], file_name)
        self.assertEqual(file2['id'], file1['id'])

        self.client.rm_by_path_if_exist(file_name)

    def test_return_none(self):
        file2 = self.client.get_file_by_id('unknown_id')
        self.assertIsNone(file2)
