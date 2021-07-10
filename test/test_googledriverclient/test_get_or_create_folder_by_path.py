import unittest
from os import path
from test.utils import SandboxTextCase

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestGetOrCreateFolderByPath(SandboxTextCase):

    def test_if_existed(self):
        folder_name = 'child'
        folder_path = self.container_path + '/middle/' + folder_name

        folder1 = self.client.create_folder_by_path(folder_path)
        self.assertIsNotNone(folder1)

        folder2 = self.client.get_or_create_folder_by_path(folder_path)
        self.assertIsNotNone(folder2)
        self.assertEqual(folder2['id'], folder1['id'])

    def test_if_not_existed(self):
        folder_name = 'child'
        folder_path = self.container_path + '/middle/' + folder_name

        folder = self.client.get_or_create_folder_by_path(folder_path)
        self.assertIsNotNone(folder)
        self.assertEqual(folder['name'], folder_name)
