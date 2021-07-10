import unittest

from googledriverclient import GoogleDriverClient


class TestGetListFile(unittest.TestCase):

    client = GoogleDriverClient()

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_eturn_success(self):
        files = self.client.get_list_file()
        self.assertTrue(len(files) > 0)

    def test_return_empty(self):
        empty_folder = self.client.get_file_by_name('empty_folder')
        files = self.client.get_list_file(parent_id=empty_folder['id'])
        self.assertTrue(len(files) == 0)
