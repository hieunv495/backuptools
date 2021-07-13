import unittest
from os import path
from test.utils import SandboxTextCase

from googledriveclient import GoogleDriveClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestCreateFolderByName(SandboxTextCase):

    def test_default(self):
        folder_name = 'child'

        folder = self.client.create_folder_by_name(
            folder_name, parent_id=self.container_file['id'])

        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], folder_name)

    def test_if_no_parent(self):
        folder_name = 'child'
        self.client.rm_by_path_if_exist(folder_name)

        folder = self.client.create_folder_by_name(
            folder_name)

        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], folder_name)

        self.client.rm_by_path(folder_name)

    def test_if_parent_not_found(self):
        folder_name = 'child'

        with self.assertRaises(ParentNotFoundException):
            self.client.create_folder_by_name(
                folder_name, parent_id='unknown_id')

    def test_if_file_existed(self):
        folder_name = 'child'
        folder_path = self.container_path + '/' + folder_name

        self.client.rm_by_path_if_exist(folder_path)

        self.client.create_folder_by_name(
            folder_name, parent_id=self.container_file['id'])

        with self.assertRaises(FileExistedException):
            self.client.create_folder_by_name(
                folder_name, parent_id=self.container_file['id'])

        self.client.rm_by_path(folder_path)
