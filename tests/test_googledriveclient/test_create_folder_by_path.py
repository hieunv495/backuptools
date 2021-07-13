import unittest
from os import path

from src.googledriveclient import GoogleDriveClient
from src.type import (FileExistedException, FileMeta, FileNotFoundException,
                      ParentNotFoundException)
from tests.utils import SandboxTextCase


class TestCreateFolderByPath(SandboxTextCase):

    def test_default(self):
        folder_name = 'child'
        folder_path = self.container_path + '/middle/' + folder_name

        folder = self.client.create_folder_by_path(folder_path)

        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], folder_name)

    def test_if_file_existed(self):
        folder_name = 'child'
        folder_path = self.container_path + '/middle/' + folder_name

        self.client.create_folder_by_path(folder_path)

        with self.assertRaises(FileExistedException):
            self.client.create_folder_by_path(folder_path)

    def test_if_parent_not_found(self):
        folder_name = 'middle'
        folder_path = self.container_path + '/middle/' + folder_name

        with self.assertRaises(ParentNotFoundException):
            self.client.create_folder_by_path(
                folder_path, auto_create_parents=False)

    def test_auto_create_parents(self):
        container_path = self.container_path + '/middle'
        folder_name = 'child'
        folder_path = self.container_path + '/middle/' + folder_name

        folder = self.client.create_folder_by_path(
            folder_path, auto_create_parents=True)

        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], folder_name)

        self.assertIsNotNone(self.client.get_file_by_path(container_path))
