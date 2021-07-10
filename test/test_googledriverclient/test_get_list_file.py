import pprint
import unittest
from test import ROOT_ID

from googledriverclient import GoogleDriverClient


class TestGetListFile(unittest.TestCase):

    client = GoogleDriverClient(root_id=ROOT_ID)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect('credentials.json')

    def test_return_success(self):
        files = self.client.get_list_file()
        self.assertIsNotNone(files)
        self.assertIsInstance(files, list)

    def test_return_empty(self):
        empty_folder = self.client.get_or_create_folder_by_path('empty_folder')
        files = self.client.get_list_file(parent_id=empty_folder['id'])
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 0)

        self.client.rm_by_id(empty_folder['id'])
