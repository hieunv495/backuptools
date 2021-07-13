import os
import unittest
from os import path
from test.utils import FileTools, SandboxTextCase, TmpFile

from googledriveclient import GoogleDriveClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestUploadFile(SandboxTextCase):

    def test_default(self):
        driver_path = self.container_path

        with TmpFile('test_default', 1024 * 2) as local_file_path:

            file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=driver_path)
            self.assertIsNotNone(file)

            file2 = self.client.get_file_by_path(
                driver_path + '/' + file['name'])
            self.assertIsNotNone(file2)

            # self.client.download_file_by_id(file['id'], './downloads')

    def test_custom_name(self):
        with TmpFile('test_default', 1024 * 2) as local_file_path:

            driver_path = self.container_path
            custom_file_name = 'ok_man.txt'
            file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=driver_path, drive_file_name=custom_file_name)
            self.assertIsNotNone(file)

            file2 = self.client.get_file_by_path(
                driver_path + '/' + custom_file_name)
            self.assertIsNotNone(file2)

            # self.client.download_file_by_id(file['id'], './downloads')

    def test_upload_to_folder_id(self):
        with TmpFile('test_default', 1024 * 2) as local_file_path:

            driver_path = self.container_path

            drive_folder_id = self.container_file['id']

            custom_file_name = 'ok_man.txt'

            file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_id=drive_folder_id, drive_file_name=custom_file_name)
            self.assertIsNotNone(file)

            file2 = self.client.get_file_by_name(
                custom_file_name, parent_id=drive_folder_id)
            self.assertIsNotNone(file2)
            self.assertEqual(file2['id'], file['id'])

            # self.client.download_file_by_id(file['id'], './downloads')

    def test_large_file(self):
        with TmpFile('test_large_file', 1024 * 1024 * 10) as local_file_path:
            driver_path = self.container_path
            file = self.client.upload_file(
                local_file_path=local_file_path, drive_folder_path=driver_path)
            self.assertIsNotNone(file)

            file2 = self.client.get_file_by_path(
                driver_path + '/' + file['name'])
            self.assertIsNotNone(file2)

            self.client.rm_by_id(file['id'])

            # self.client.download_file_by_id(file['id'], './downloads')
