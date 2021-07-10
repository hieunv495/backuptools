import unittest

from backupclient import BackupClient


class TestBackupClient(unittest.TestCase):

    client = BackupClient(
        credentials_path='credentials.json', driver_root_folder_name='test', local_root_folder_path="/data/backups_test")

    def test_get_root_folder(self):
        file = self.client.get_root_folder()
        self.assertIsNotNone(file)

    def test_get_list_app(self):
        apps = self.client.get_list_app()
        self.assertIsNotNone(apps)

    def test_get_app_folder_return_success(self):
        folder = self.client.get_app_folder('app1')
        self.assertIsNotNone(folder)

    def test_get_app_folder_return_none(self):
        folder = self.client.get_app_folder('app_not_exist')
        self.assertIsNone(folder)

    def test_get_list_resource_return_success(self):
        resources = self.client.get_list_resource('app1')
        self.assertIsNotNone(resources)
        self.assertTrue(len(resources) > 0)

    def test_get_list_resource_return_empty(self):
        resources = self.client.get_list_resource('app2')
        self.assertIsNotNone(resources)
        self.assertTrue(len(resources) == 0)

    def test_get_resource_folder_return_success(self):
        folder = self.client.get_resource_folder('app1', 'resource1')
        self.assertIsNotNone(folder)

    def test_get_resource_folder_return_none(self):
        folder = self.client.get_resource_folder('app1', 'resource_not_exist')
        self.assertIsNone(folder)

    def test_download_backup(self):
        pass

# if __name__ == '__main__':
#     unittest.main(verbosity=2)
