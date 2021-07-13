import pprint
import unittest

from src.googledriveclient import GoogleDriveClient
from tests import CREDENTIALS_PATH, ROOT_ID


class TestGetListFile(unittest.TestCase):

    client = GoogleDriveClient(root_id=ROOT_ID)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect(CREDENTIALS_PATH)

    def test_with_no_parent(self):
        files = self.client.get_list_file()

        self.assertIsNotNone(files)
        self.assertIsInstance(files, list)

    def test_with_parent_id(self):

        # CREATE TEST DATA
        self.client.rm_by_path_if_exist(self.id())
        parent = self.client.get_or_create_folder_by_path(self.id())
        self.assertIsNotNone(parent)

        created_names = ['child1', 'child2']

        for name in created_names:
            self.client.get_or_create_folder_by_path(
                '{0}/{1}'.format(self.id(), name))

        # TEST
        files = self.client.get_list_file(parent_id=parent['id'])
        self.assertIsNotNone(files)
        self.assertIsInstance(files, list)

        file_names = [file['name'] for file in files]

        self.assertListEqual(sorted(file_names), sorted(created_names))

        # REMOVE TEST DATA
        self.client.rm_by_path_if_exist(self.id())

    def test_with_parent_path(self):

        # CREATE TEST DATA
        self.client.rm_by_path_if_exist(self.id())
        parent = self.client.get_or_create_folder_by_path(self.id())
        self.assertIsNotNone(parent)

        created_names = ['child1', 'child2']

        for name in created_names:
            self.client.get_or_create_folder_by_path(
                '{0}/{1}'.format(self.id(), name))

        # TEST
        files = self.client.get_list_file(parent_path=self.id())
        self.assertIsNotNone(files)
        self.assertIsInstance(files, list)

        file_names = [file['name'] for file in files]

        self.assertListEqual(sorted(file_names), sorted(created_names))

        # REMOVE TEST DATA
        self.client.rm_by_path_if_exist(self.id())

    def test_return_empty(self):
        empty_folder = self.client.get_or_create_folder_by_path(self.id())
        files = self.client.get_list_file(parent_id=empty_folder['id'])
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 0)

        self.client.rm_by_id(empty_folder['id'])
