import unittest
from os import path
from test.utils import SandboxTextCase

from googledriverclient import GoogleDriverClient
from type import (FileExistedException, FileMeta, FileNotFoundException,
                  ParentNotFoundException)


class TestUploadFile(SandboxTextCase):

    def test_default(self):
        driver_path = self.container_path
        file = self.client.upload_file(
            local_file_path="./example-files/example.txt", drive_folder_path=driver_path)
        self.assertIsNotNone(file)

        file2 = self.client.get_file_by_path(driver_path + '/' + file['name'])
        self.assertIsNotNone(file2)

        self.client.download_file_by_id(file['id'], './downloads')

    def test_custom_name(self):
        driver_path = self.container_path
        custom_file_name = 'ok_man.txt'
        file = self.client.upload_file(
            local_file_path="./example-files/example.txt", drive_folder_path=driver_path, drive_file_name=custom_file_name)
        self.assertIsNotNone(file)

        file2 = self.client.get_file_by_path(
            driver_path + '/' + custom_file_name)
        self.assertIsNotNone(file2)

        self.client.download_file_by_id(file['id'], './downloads')

    def test_large_file(self):
        driver_path = 'test/backups-test'
        file = self.client.upload_file(
            local_file_path="/data/beebook/backups/2021-07-07/beebook-mongo.tar.gz", drive_folder_path=driver_path)
        self.assertIsNotNone(file)

        file2 = self.client.get_file_by_path(driver_path + '/' + file['name'])
        self.assertIsNotNone(file2)

        # self.client.download_file_by_id(file['id'], './downloads')
