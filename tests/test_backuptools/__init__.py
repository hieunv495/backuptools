import os
import pprint
import shutil
import unittest

from checksumdir import dirhash
from src.backuptools import BackupTools
from src.googledriveclient import GoogleDriveClient
from tests import CREDENTIALS_PATH, ROOT_ID
from tests.utils import FileTools


class TestBackupTools(unittest.TestCase):

    # config = {
    #     "drive_credentials": "credentials.json",
    #     "drive_root_id": "1rbi0gr7yMAFKqEgx-pBp6kKJx1Z4Tcgm",
    #     "resources": [
    #         {
    #             "type": "GoogleDriveBackupResource",
    #             "name": "resource1",
    #             "args": {
    #                 "local_resource_path": "./tmp/resources/resource1",
    #                 "local_backup_folder_path": "./tmp/backups/resource1",
    #                 "drive_backup_folder_path": "backups/resource1"
    #             }
    #         }
    #     ]
    # }

    # backup_tools = BackupTools(config)

    drive_client = GoogleDriveClient(root_id=ROOT_ID)

    def setUp(self):
        resource_name = self.id().replace('.', '-')
        self.config = {
            "drive_credentials": CREDENTIALS_PATH,
            "drive_root_id": ROOT_ID,
            "resources": [
                {
                    "type": "GoogleDriveBackupResource",
                    "name": resource_name,
                    "args": {
                        "local_resource_path": "./tmp/resources/" + resource_name,
                        "local_backup_folder_path": "./tmp/backups/" + resource_name,
                        "drive_backup_folder_path": "backups/" + resource_name
                    }
                }
            ]
        }

        self.resource_info = self.config['resources'][0]

        self.backup_tools = BackupTools(self.config)

        if not self.drive_client.is_connected:
            self.drive_client.connect(CREDENTIALS_PATH)

        self._create_test_resource()

    def tearDown(self):
        self._remove_test_resource()
        self._remove_drive_backup_folder()

    def _get_test_resource_path(self):
        return self.config['resources'][0]['args']['local_resource_path']

    def _create_test_resource(self):

        resource_path = self._get_test_resource_path()

        os.makedirs(resource_path, exist_ok=True)

        file_names = ['file1', 'file2']
        file_paths = [os.path.join(resource_path, file_name)
                      for file_name in file_names]

        file_size = 1024

        for path in file_paths:
            FileTools.create_file(path, file_size)

        return self.config['resources'][0]

    def _remove_test_resource(self):
        resource_path = self._get_test_resource_path()
        shutil.rmtree(resource_path)
        shutil.rmtree(self.config['resources'][0]
                      ['args']['local_backup_folder_path'])

    def _remove_drive_backup_folder(self):
        drive_backup_path = self.resource_info['args']['drive_backup_folder_path']
        self.drive_client.rm_by_path_if_exist(drive_backup_path)

    def test_backup_file_name(self):
        version = self.backup_tools.exec(
            self.resource_info['name'], 'generate_version_key')
        self.assertIsNotNone(version)

        backup_file_name = self.backup_tools.exec(
            self.resource_info['name'], 'get_backup_file_name', version)
        self.assertIsNotNone(backup_file_name)

        getted_version = self.backup_tools.exec(
            self.resource_info['name'], 'get_version_from_backup_file_name', backup_file_name)
        self.assertIsNotNone(getted_version)

        self.assertEqual(version, getted_version)

    def test_create_version(self):

        version = self.backup_tools.exec(
            self.resource_info['name'], 'create_version')

        local_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_local_backup_file_path', version)

        # CHECK BACKUP FILE EXISTS
        self.assertTrue(os.path.isfile(local_backup_file_path))

    def test_extract_version(self):

        # CREATE BACKUP
        version = self.backup_tools.exec(
            self.resource_info['name'], 'create_version')

        local_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_local_backup_file_path', version)

        # CHECK BACKUP FILE EXISTS
        self.assertTrue(os.path.isfile(local_backup_file_path))

        # BEFORE HASH
        before_hash = dirhash(self._get_test_resource_path())

        # REMOVE RESOURCE
        shutil.rmtree(self._get_test_resource_path())

        # EXTRACT RESOURCE
        self.backup_tools.exec(
            self.resource_info['name'], 'extract_version', version)

        # CHECK RESOURCE EXISTS
        self.assertTrue(os.path.exists(self._get_test_resource_path()))

        # AFTER HASH
        after_hash = dirhash(self._get_test_resource_path())

        self.assertEqual(before_hash, after_hash)

    def test_upload_version(self):

        # CREATE BACKUP
        version = self.backup_tools.exec(
            self.resource_info['name'], 'create_version')

        drive_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_drive_backup_file_path', version)

        # UPLOAD BACKUP
        self.backup_tools.exec(
            self.resource_info['name'], 'upload_version', version)

        # CHECK DRIVE BACKUP FILE EXIST
        drive_client = GoogleDriveClient(root_id=ROOT_ID)
        drive_client.connect(CREDENTIALS_PATH)

        drive_backup_file = drive_client.get_file_by_path(
            drive_backup_file_path)

        self.assertIsNotNone(drive_backup_file)

    def test_download_version(self):

        # CREATE BACKUP
        version = self.backup_tools.exec(
            self.resource_info['name'], 'create_version')

        local_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_local_backup_file_path', version)

        # UPLOAD BACKUP
        self.backup_tools.exec(
            self.resource_info['name'], 'upload_version', version)

        # REMOVE LOCAL BACKUP
        os.remove(local_backup_file_path)

        # DOWNLOAD BACKUP
        self.backup_tools.exec(
            self.resource_info['name'], 'download_version', version)

        # CHECK LOCAL BACKUP FILE EXIST
        self.assertTrue(os.path.exists(local_backup_file_path))

    def test_backup(self):

        # BACKUP
        version = self.backup_tools.exec(
            self.resource_info['name'], 'backup')

        local_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_local_backup_file_path', version)

        drive_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_drive_backup_file_path', version)

        # CHECK LOCAL BACKUP FILE
        self.assertTrue(os.path.isfile(local_backup_file_path))

        # CHECK DRIVE BACKUP FILE
        drive_client = GoogleDriveClient(root_id=ROOT_ID)
        drive_client.connect(CREDENTIALS_PATH)

        drive_backup_file = drive_client.get_file_by_path(
            drive_backup_file_path)

        self.assertIsNotNone(drive_backup_file)

    def test_restore(self):
        # BACKUP
        version = self.backup_tools.exec(
            self.resource_info['name'], 'backup')

        local_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_local_backup_file_path', version)

        drive_backup_file_path = self.backup_tools.exec(
            self.resource_info['name'], 'get_drive_backup_file_path', version)

        # BEFORE HASH
        before_hash = dirhash(self._get_test_resource_path())

        # REMOVE LOCAL BACKUP
        os.remove(local_backup_file_path)

        # REMOVE LOCAL SOURCE
        shutil.rmtree(self._get_test_resource_path())

        # RESTORE
        self.backup_tools.exec(
            self.resource_info['name'], 'restore', version)

        # CHECK LOCAL BACKUP FILE EXIST
        self.assertTrue(os.path.exists(local_backup_file_path))

        # CHECK RESOURCE EXISTS
        self.assertTrue(os.path.exists(self._get_test_resource_path()))

        # AFTER HASH
        after_hash = dirhash(self._get_test_resource_path())

        self.assertEqual(before_hash, after_hash)

    def test_list_local_version(self):

        # CREATE BACKUP 1
        version1 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v1')

        # CREATE BACKUP 2
        version2 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v2')

        # LIST LOCAL VERSION
        local_versions = self.backup_tools.exec(
            self.resource_info['name'], 'list_local_version')

        # CHECK LIST LOCAL VERSION CORRECT
        self.assertListEqual(sorted(local_versions), sorted(['v1', 'v2']))

    def test_list_drive_version(self):
        # CREATE BACKUP 1
        version1 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v1')

        # CREATE BACKUP 2
        version2 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v2')

        # LIST DRIVE VERSION
        drive_versions = self.backup_tools.exec(
            self.resource_info['name'], 'list_drive_version')

        # CHECK LIST DRIVE VERSION CORRECT
        self.assertListEqual(sorted(drive_versions), sorted(['v1', 'v2']))

    def test_remove_local_version(self):
        # CREATE BACKUP 1
        version1 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v1')

        # CREATE BACKUP 2
        version2 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v2')

        # REMOVE LOCAL VERSION
        self.backup_tools.exec(
            self.resource_info['name'], 'remove_local_version', 'v1')

        # LIST LOCAL VERSION
        local_versions = self.backup_tools.exec(
            self.resource_info['name'], 'list_local_version')

        # CHECK LIST LOCAL VERSION CORRECT
        self.assertListEqual(sorted(local_versions), sorted(['v2']))

    def test_remove_drive_version(self):
        # CREATE BACKUP 1
        version1 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v1')

        # CREATE BACKUP 2
        version2 = self.backup_tools.exec(
            self.resource_info['name'], 'backup', 'v2')

        # REMOVE DRIVE VERSION
        self.backup_tools.exec(
            self.resource_info['name'], 'remove_drive_version', 'v1')

        # LIST DRIVE VERSION
        drive_versions = self.backup_tools.exec(
            self.resource_info['name'], 'list_drive_version')

        # CHECK LIST DRIVE VERSION CORRECT
        self.assertListEqual(sorted(drive_versions), sorted(['v2']))
