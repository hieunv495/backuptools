from __future__ import print_function

import os.path
import pprint
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googledriverclient import GoogleDriverClient
from type import FileMeta

'''
https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html
'''


class BackupClient:

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.metadata']

    service = None
    driver_client = GoogleDriverClient()
    driver_root_folder_name = None
    local_root_folder_path = None

    def __init__(self, credentials_path: str = None, driver_root_folder_name: str = None, local_root_folder_path: str = None):
        self.driver_client.connect(credentials_path)
        self.driver_root_folder_name = driver_root_folder_name
        self.local_root_folder_name = local_root_folder_path

    def get_root_folder(self) -> Optional[FileMeta]:
        return self.driver_client.get_file_by_name(self.driver_root_folder_name)

    def get_list_app(self) -> Optional[List[FileMeta]]:
        root_folder = self.get_root_folder()
        if root_folder is None:
            return None
        return self.driver_client.get_list_file(parent_id=root_folder['id'])

    def get_app_folder(self, app_name: str) -> Optional[FileMeta]:
        root_folder = self.get_root_folder()
        if root_folder is None:
            return None
        return self.driver_client.get_file_by_name(app_name, parent_id=root_folder['id'])

    def get_list_resource(self, app_name: str) -> Optional[List[FileMeta]]:
        app_folder = self.get_app_folder(app_name)
        if app_folder is None:
            return None
        return self.driver_client.get_list_file(parent_id=app_folder['id'])

    def get_resource_folder(self, app_name: str, resource_name: str) -> Optional[FileMeta]:
        app_folder = self.get_app_folder(app_name)
        if app_folder is None:
            return None
        return self.driver_client.get_file_by_name(resource_name, parent_id=app_folder['id'])

    def get_backup_file(self, app_name: str, resource_name: str, backup_version: str) -> Optional[FileMeta]:
        resource_folder = self.get_resource_folder(app_name, resource_name)
        if resource_folder is None:
            return None
        return self.driver_client.get_file_by_name(
            backup_version, parent_id=resource_folder['id'])

    def download_backup(self, app_name: str, resource_name: str, backup_version: str) -> str:
        # check or create resource folder
        pass

    def upload_backup(self, app_name: str, resource_name: str, backup_version: str) -> str:
        pass
