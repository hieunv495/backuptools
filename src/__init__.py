import json
import pprint
import sys

from .backuptools import BackupResource, BackupTools
from .googledriveclient import GoogleDriveClient

if __name__ == '__main__':
    config_file = sys.argv[1]
    args = sys.argv[2:]

    config: dict = None

    with open(config_file) as f:
        config = json.load(f)

    tools = BackupTools(config)

    result = tools.exec(*args)

    pprint.pprint(result)
