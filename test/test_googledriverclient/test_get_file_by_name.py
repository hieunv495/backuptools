import unittest

from googledriverclient import GoogleDriverClient


class TestGetFileByName(unittest.TestCase):

    client = GoogleDriverClient()

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_return_success(self):
        file = self.client.get_file_by_name('test')
        self.assertIsNotNone(file)

    def test_return_none(self):
        file = self.client.get_file_by_name('test_not_exist')
        self.assertIsNone(file)

    def test_with_parent_return_success(self):
        root_folder = self.client.get_file_by_name('test')
        file = self.client.get_file_by_name(
            'test1', parent_id=root_folder['id'])
        self.assertIsNotNone(file)

    def test_with_parent_return_none(self):
        root_folder = self.client.get_file_by_name('test')
        file = self.client.get_file_by_name(
            'unknown_folder', parent_id=root_folder['id'])
        self.assertIsNone(file)
