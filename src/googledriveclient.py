from __future__ import print_function

import io
import os
import pprint
import traceback
from os import path
from typing import List, Optional, Union

import magic
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .type import (FileExistedException, FileMeta, FileNotFoundException,
                   ParentNotFoundException)

'''
https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html
'''


class GoogleDriveClient:

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.metadata']

    service = None
    is_connected = False

    def __init__(self, root_id: str = None):
        self.root_id = root_id

    def connect(self, credentials_path: str):
        creds = service_account.Credentials.from_service_account_file(
            credentials_path)
        # print('Connect')
        # client = build("drive", "v3", credentials=creds)
        # client._http.http.close()

        self.service = build('drive', 'v3', credentials=creds)
        # print('Connect success')
        # self.service._http.http.close()
        self.is_connected = True

    def get_list_file(self, parent_id: str = None, parent_path: str = None, file_fields: str = 'id,name,size') -> List[FileMeta]:

        if parent_id is not None and parent_path is not None:
            raise ValueError(
                'Only one of "parent_id" or "parent_path" should be provided')

        if parent_path is not None:
            parent = self.get_file_by_path(parent_path)
            if parent is None:
                raise FileNotFoundException(
                    'Parent path "{0}" not found'.format(parent_path))
            parent_id = parent['id']

        parent_id = parent_id or self.root_id
        q = ''
        if parent_id is not None:
            q = "'{0}' in parents".format(parent_id)

        results = self.service.files().list(
            q=q,
            fields='nextPageToken, files({file_fields})'.format(file_fields=file_fields)).execute()

        items = results.get('files', [])

        return items

    def get_file_by_id(self, file_id: str) -> Union[FileMeta, None]:
        try:
            results = self.service.files().get(fileId=file_id).execute()
            file: FileMeta = {
                'id': results.get('id'),
                'name': results.get('name')
            }
            return file
        except Exception as e:
            # traceback.print_exc()
            return None

    def get_file_by_name(self, name: str, parent_id: Optional[str] = None) -> Union[FileMeta, None]:

        parent_id = parent_id or self.root_id

        if parent_id:
            if self.get_file_by_id(parent_id) is None:
                raise ParentNotFoundException()

        q = ''
        if parent_id is None:
            q = "name='{0}'".format(name)
        else:
            q = u"'{0}' in parents and name='{1}'".format(parent_id, name)

        results = self.service.files().list(
            q=q,
            pageSize=1,
            fields='nextPageToken, files(id,name)').execute()

        items = results.get('files', [])

        if(len(items) > 0):
            return items[0]
        else:
            return None

    def get_file_by_path(self, path: str, parent_id: Optional[str] = None) -> Union[FileMeta, None]:

        parent_id = parent_id or self.root_id

        parent: Optional[FileMeta] = None

        if parent_id is not None:
            parent = self.get_file_by_id(parent_id)
            if parent is None:
                raise ParentNotFoundException()

        bits = path.split('/')
        current_file: Optional[FileMeta] = parent
        for name in bits:
            current_file = self.get_file_by_name(
                name, parent_id=current_file['id'] if current_file is not None else None)
            if current_file is None:
                return None
        return current_file

    def download_file_by_id(self, file_id: str, local_folder_path, local_file_name: Optional[str] = None) -> Union[str, None]:

        if local_file_name is None:
            file = self.get_file_by_id(file_id)
            if file is None:
                return None
            local_file_name = file['name']

        local_file_path = path.abspath(
            path.join(local_folder_path, local_file_name))

        request = self.service.files().get_media(fileId=file_id)

        if os.path.exists(local_folder_path):
            if not os.path.isdir(local_folder_path):
                raise Exception('{0} not is folder'.format(local_folder_path))
        else:
            os.mkdir(local_folder_path)

        with open(local_file_path, 'wb') as fh:
            # fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

        return local_file_path

    def download_file_by_path(self, drive_file_path: str, local_folder_path: str, local_file_name: Optional[str] = None) -> Union[str, None]:
        file = self.get_file_by_path(drive_file_path)
        if file is None:
            raise Exception('File not found')

        return self.download_file_by_id(
            file['id'], local_folder_path, local_file_name=local_file_name)

    def rm_by_id(self, file_id: str):
        return self.service.files().delete(fileId=file_id).execute()

    def rm_by_path(self, path: str):
        file = self.get_file_by_path(path)
        if file is None:
            raise Exception('File not found')
        return self.rm_by_id(file['id'])

    def rm_by_path_if_exist(self, path: str):
        file = self.get_file_by_path(path)
        if file is not None:
            return self.rm_by_id(file['id'])

    def create_folder_by_name(self, name: str, parent_id: Optional[str] = None) -> Union[FileMeta, None]:

        parent_id = parent_id or self.root_id

        exist_folder = self.get_file_by_name(name, parent_id=parent_id)
        if exist_folder is not None:
            raise FileExistedException()

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }

        file = self.service.files().create(body=file_metadata, fields='id,name').execute()

        return file

    def create_folder_by_path(self, path: str, auto_create_parents: bool = True) -> Union[FileMeta, None]:
        names = path.split('/')
        current_folder: FileMeta = self.get_file_by_id(self.root_id)
        if current_folder is None:
            raise FileNotFoundException(
                'Root folder not found "{0}"'.format(self.root_id))
        path_len = len(names)
        for index, name in enumerate(names):
            current_folder_id = current_folder['id'] if current_folder is not None else None
            folder = self.get_file_by_name(
                name, parent_id=current_folder_id)
            is_parent = index < path_len - 1

            if is_parent:
                if folder is None:
                    if auto_create_parents:
                        folder = self.create_folder_by_name(
                            name, parent_id=current_folder_id)
                    else:
                        raise ParentNotFoundException('Folder {path} not found'.format(
                            path='/'.join(names[:index + 1])))
            else:
                if folder is not None:
                    raise FileExistedException()
                else:
                    folder = self.create_folder_by_name(
                        name, parent_id=current_folder_id)

            current_folder = folder

        return current_folder

    def get_or_create_folder_by_path(self, path: str, auto_create_parents: bool = True) -> Union[FileMeta, None]:
        folder = self.get_file_by_path(path)
        if folder is not None:
            return folder
        else:
            return self.create_folder_by_path(path, auto_create_parents=auto_create_parents)

    def upload_file(self, local_file_path: str = None, drive_folder_path: str = None, drive_folder_id: str = None, drive_file_name: Optional[str] = None) -> Union[FileMeta, None]:

        if drive_folder_id is None and drive_folder_path is None:
            raise Exception(
                'One of driver_folder_path or driver_folder_id must provided')

        if drive_folder_id is not None and drive_folder_path is not None:
            raise Exception(
                'Can only choose one of "driver_folder_path" or "driver_folder_id"')

        file_name = drive_file_name or path.basename(local_file_path)

        drive_folder: FileMeta = None

        if drive_folder_path is not None:
            file_drive_path = path.join(drive_folder_path, file_name)

            exist_folder = self.get_file_by_path(file_drive_path)
            if exist_folder is not None:
                raise FileExistedException()

            drive_folder = self.get_or_create_folder_by_path(
                drive_folder_path)

        elif drive_folder_id:

            exist_folder = self.get_file_by_name(
                file_name, parent_id=drive_folder_id)
            if exist_folder is not None:
                raise FileExistedException()

            drive_folder = self.get_file_by_id(
                drive_folder_id)

            if drive_folder is None:
                raise FileNotFoundException(
                    'Drive folder not found by folder id "{0}"'.format(drive_folder_id))

        file_metadata = {
            'name': file_name,
            'parents': [drive_folder['id']]
        }

        mimetype = magic.from_file(local_file_path, mime=True)
        media = MediaFileUpload(
            local_file_path, mimetype=mimetype, resumable=True)

        request = self.service.files().create(
            body=file_metadata, media_body=media, fields='id,name')

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))

        print("Upload Complete!")

        return response
