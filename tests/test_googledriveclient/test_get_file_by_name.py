import os
import unittest

from src.googledriveclient import GoogleDriveClient
from tests import CREDENTIALS_PATH, ROOT_ID


class TestGetFileByName(unittest.TestCase):

    client = GoogleDriveClient(root_id=ROOT_ID)

    def __init__(self, methodName):
        super().__init__(methodName)
        self.client.connect(CREDENTIALS_PATH)

    def test_with_no_parent(self):
        file_name = 'test_with_no_parent'
        created = self.client.get_or_create_folder_by_path(file_name)
        self.assertIsNotNone(created)

        file = self.client.get_file_by_name(file_name)
        self.assertIsNotNone(file)

        self.client.rm_by_id(created['id'])

    def test_return_none(self):
        self.client.rm_by_path_if_exist('not_exist_file')

        file = self.client.get_file_by_name('not_exist_file')
        self.assertIsNone(file)

    def test_with_parent(self):
        container_folder_path = 'test_get_file_by_name_container_folder'

        container_folder = self.client.get_or_create_folder_by_path(
            container_folder_path
        )
        self.assertIsNotNone(container_folder)

        child_folder_name = 'child'
        child_folder_path = os.path.join(
            container_folder_path, child_folder_name)

        child_folder = self.client.get_or_create_folder_by_path(
            child_folder_path)
        self.assertIsNotNone(child_folder)

        file = self.client.get_file_by_name(
            child_folder_name, parent_id=container_folder['id'])
        self.assertIsNotNone(file)

        self.client.rm_by_id(child_folder['id'])
        self.client.rm_by_id(container_folder['id'])

    def test_with_parent_return_none(self):
        container_folder = self.client.get_or_create_folder_by_path(
            'test_with_parent_return_none')
        self.assertIsNotNone(container_folder)

        file = self.client.get_file_by_name(
            'unknown_folder', parent_id=container_folder['id'])
        self.assertIsNone(file)

        self.client.rm_by_id(container_folder['id'])
