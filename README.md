# backup-tools

Backup, restore, version control local data to google drive

# Prerequisites

- Python >= 3.6

# Install

```bash
pip install backuptools
```

# Usage

## Create config file

1. Create and download google account service json file **credentials.json** for **google drive service**

Create `config.json` with content:

```json
{
  "drive_credentials": "<path/to/credentials.json>",
  "drive_root_id": "<id_of_drive_folder>",
  "resources": [
    {
      "type": "GoogleDriveBackupResource",
      "name": "<resource_name>",
      "args": {
        "local_resource_path": "<path/to/local/source>",
        "local_backup_folder_path": "<path/to/local/backup/folder>",
        "drive_backup_folder_path": "<path/to/drive/backup/folder>"
      }
    }
  ]
}
```

## Backup

```bash
python -m backuptools <path/to/config.json> <resource> backup [<version>]
```

## Restore

```bash
python -m backuptools <path/to/config.json> <resource> restore <version>
```

## List local version

```bash
python -m backuptools <path/to/config.json> <resource> list_local_version
```

## List drive version

```bash
python -m backuptools <path/to/config.json> <resource> list_local_version
```

## Create local version

```bash
python -m backuptools <path/to/config.json> <resource> create_version [<version>]
```

## Extract local version

```bash
python -m backuptools <path/to/config.json> <resource> extract <version>
```

## Upload version

```bash
python -m backuptools <path/to/config.json> <resource> upload_version <version>
```

## Download version

```bash
python -m backuptools <path/to/config.json> <resource> download_version <version>
```

## Remove local version

```bash
python -m backuptools <path/to/config.json> <resource> remove_local_version <version>
```

## Remove drive version

```bash
python -m backuptools <path/to/config.json> <resource> remove_drive_version <version>
```

# Development

## Prerequisites

```bash
pip3 install virtualenv
virtualenv .env
source .env/bin/activate
pip install requirements.txt
```

### Install packages

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Test

1. Create and download google account service json file **credentials/credentials.json** for **google drive service**

2. Create file `test/local_config.py` with content:

```python
ROOT_ID = "1rbi0gr7yMAFKqEgx-pBp6kKJx1Z4Tcgm"
CREDENTIALS_PATH = 'credentials/credentials.json'

```

3. Test command line

```
./test.sh
```

## h
