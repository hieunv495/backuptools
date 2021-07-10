import unittest
from os import path
from test.utils import SandboxTextCase, TmpFile

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestDownloadFileById(SandboxTextCase):

    def test_with_default_name(self):

        with TmpFile('file_tmp', 1024) as local_file_path:
            uploaded_file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=self.container_path)

            downloaded_file_path = self.client.download_file_by_id(
                uploaded_file['id'], local_folder_path='./downloads')

            self.assertIsNotNone(downloaded_file_path)
            self.assertTrue(path.isabs(downloaded_file_path))
            self.assertTrue(path.isfile(downloaded_file_path))
            self.assertEqual(path.basename(
                downloaded_file_path), uploaded_file['name'])

    def test_with_custom_name(self):

        with TmpFile('file_tmp', 1024) as local_file_path:
            uploaded_file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=self.container_path)

            custom_name = 'test-custom-name.txt'

            downloaded_file_path = self.client.download_file_by_id(
                uploaded_file['id'], local_folder_path='./downloads', local_file_name=custom_name)

            self.assertIsNotNone(downloaded_file_path)
            self.assertTrue(path.isabs(downloaded_file_path))
            self.assertTrue(path.isfile(downloaded_file_path))
            self.assertEqual(path.basename(downloaded_file_path), custom_name)
