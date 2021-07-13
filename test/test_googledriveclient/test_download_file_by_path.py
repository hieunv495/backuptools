import unittest
from os import path
from test import ROOT_ID
from test.utils import SandboxTextCase, TmpFile

from googledriveclient import GoogleDriveClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestDownloadFileByPath(SandboxTextCase):

    def test_with_default_name(self):

        with TmpFile('file_tmp', 1024) as local_file_path:
            uploaded_file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=self.container_path)

            driver_file_path = path.join(self.container_path, 'file_tmp')
            file = self.client.get_file_by_path(driver_file_path)

            self.assertIsNotNone(file)

            downloaded_file_path = self.client.download_file_by_path(
                driver_file_path, local_folder_path='./downloads')

            self.assertIsNotNone(downloaded_file_path)
            self.assertTrue(path.isabs(downloaded_file_path))
            self.assertTrue(path.isfile(downloaded_file_path))
            self.assertEqual(path.basename(downloaded_file_path), file['name'])

    def test_with_custom_name(self):

        with TmpFile('file_tmp', 1024) as local_file_path:
            uploaded_file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=self.container_path)

            driver_file_path = path.join(self.container_path, 'file_tmp')
            file = self.client.get_file_by_path(driver_file_path)

            self.assertIsNotNone(file)

            custom_name = 'test-custom-name.txt'

            downloaded_file_path = self.client.download_file_by_path(
                driver_file_path, local_folder_path='./downloads', local_file_name=custom_name)

            self.assertIsNotNone(downloaded_file_path)
            self.assertTrue(path.isabs(downloaded_file_path))
            self.assertTrue(path.isfile(downloaded_file_path))
            self.assertEqual(path.basename(downloaded_file_path), custom_name)
