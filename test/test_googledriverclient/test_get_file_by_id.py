import unittest

from googledriverclient import GoogleDriverClient


class TestGetFileById(unittest.TestCase):

    client = GoogleDriverClient()

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_return_success(self):
        file1 = self.client.get_file_by_name('test')
        self.assertIsNotNone(file1)
        file2 = self.client.get_file_by_id(file1['id'])
        self.assertIsNotNone(file2)
        self.assertEqual(file2['name'], 'test')
        self.assertEqual(file2['id'], file1['id'])

    def test_return_none(self):
        file2 = self.client.get_file_by_id('unknown_id')
        self.assertIsNone(file2)
