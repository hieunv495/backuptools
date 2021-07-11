import datetime
import json
import os
import pprint
import sys
import tarfile
from typing import List

from googledriverclient import GoogleDriverClient


class GoogleDriveBackupResource():

    default_local_backup_folder_path = '/data/backups'

    def __init__(self, name: str = None, local_source_path: str = None, drive_credentials: str = None, drive_root_id: str = None, drive_backup_folder_path: str = None, drive_backup_folder_id: str = None, local_backup_folder_path: str = None, remove_after_backup: bool = False, remove_after_restore: bool = False):
        self.name = name
        self.local_source_path = os.path.abspath(local_source_path)

        self.drive_credentials = drive_credentials
        self.drive_root_id = drive_root_id
        self.drive_backup_folder_path = drive_backup_folder_path
        self.drive_backup_folder_id = drive_backup_folder_id

        self.remove_after_backup = remove_after_backup
        self.remove_after_restore = remove_after_restore

        self.local_backup_folder_path = os.path.abspath(
            local_backup_folder_path) if local_backup_folder_path is not None else self.default_local_backup_folder_path

        self._drive_client: GoogleDriverClient = None

        self._prepare_folder()

    def _prepare_folder(self):
        if os.path.exists(self.local_backup_folder_path):
            if not os.path.isdir(self.local_backup_folder_path):
                raise Exception('local_backup_folder_path "{0}" is not folder')
        else:
            os.makedirs(self.local_backup_folder_path)

    @property
    def drive_client(self):
        if self._drive_client is None:
            self._drive_client = GoogleDriverClient(root_id=self.drive_root_id)
            self._drive_client.connect(self.drive_credentials)

        return self._drive_client

    def get_local_backup_file_path(self, version: str) -> str:
        return os.path.join(self.local_backup_folder_path, '{0}-{1}.tar.gz'.format(self.name, version))

    def get_drive_backup_file_path(self, version: str) -> str:
        return os.path.join(self.drive_backup_folder_path, '{0}-{1}.tar.gz'.format(self.name, version))

    def create_backup(self, version: str):
        file_path = self.get_local_backup_file_path(version)
        with tarfile.open(file_path, 'w:gz') as tar:
            tar.add(self.local_source_path,
                    arcname=os.path.basename(self.local_source_path))
        return file_path

    def extract_backup(self, version: str):
        file_path = self.get_local_backup_file_path(version)
        source_folder = os.path.dirname(self.local_source_path)
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(source_folder)

    def remove_local_backup(self, version: str):
        backup_path = self.get_local_backup_file_path(version)
        os.remove(backup_path)

    def download_backup(self, version: str):
        self.drive_client.download_file_by_path(drive_file_path=self.get_drive_backup_file_path(
            version), local_folder_path=self.local_backup_folder_path)

    def upload_backup(self, version: str):
        self.drive_client.upload_file(local_file_path=self.get_local_backup_file_path(
            version), drive_folder_path=self.drive_backup_folder_path)

    def backup(self, version: str = None):
        if version is None:
            now = datetime.datetime.now()
            version = '{0}-{1}-{2}-{3}-{4}-{5}'.format(
                now.year, now.month, now.day, now.hour, now.minute, now.second)

        self.create_backup(version)
        self.upload_backup(version)
        if self.remove_after_backup:
            self.remove_local_backup(version)

    def restore(self, version):
        self.download_backup(version)
        self.extract_backup(version)
        if self.remove_after_restore:
            self.remove_local_backup(version)

    def list_local_version(self) -> List[str]:
        return [f for f in os.listdir(self.local_backup_folder_path) if os.path.isfile(os.path.join(self.local_backup_folder_path, f))]

    def list_drive_version(self):
        files = self.drive_client.get_list_file(
            parent_path=self.drive_backup_folder_path)
        return [file['name'] for file in files]


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


class BackupTools():

    def __init__(self, config_file: str = None):

        self.resources: list = []
        self.config: dict = None

        with open(config_file) as f:
            self.config = json.load(f)

        self.drive_credentials = self.config.get('drive_credentials')
        self.drive_root_id = self.config.get('drive_root_id')

        self._build_resources()

    def _get_resource(self, data):
        resource_type = data.get('type')
        resource_name = data.get('name')
        resource_args = data.get('args')
        if resource_type == 'GoogleDriveBackupResource':
            resource_args['drive_credentials'] = resource_args.get(
                'drive_credentials') or self.drive_credentials

            resource_args['drive_root_id'] = resource_args.get(
                'drive_root_id') or self.drive_root_id

            return GoogleDriveBackupResource(name=resource_name, **resource_args)

    def _build_resources(self):
        self.resources = [self._get_resource(
            item) for item in self.config.get('resources')]

    def exec(self, *args):

        resource_name = None
        method_name = None
        method_args = None
        resource = None
        method = None

        if len(args) == 0:
            pprint.pprint(self.config)
            return

        resource_name = args[0]
        resource = next(
            (item for item in self.resources if item.name == resource_name), None)
        if resource is None:
            raise Exception(
                'Resource "{0}" not found'.format(resource_name))

        method_name = args[1]

        method = getattr(resource, method_name)
        if method is None:
            raise Exception('Method "{0}.{1}" not found'.format(
                resource_name, method_name))

        if not callable(method):
            raise Exception('Method "{0}.{1}" not callable'.format(
                resource_name, method_name))

        method_args = args[2:]

        return method(*method_args)


if __name__ == '__main__':
    config_file = sys.argv[1]
    args = sys.argv[2:]

    tools = BackupTools(config_file)

    result = tools.exec(*args)

    pprint.pprint(result)
