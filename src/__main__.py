import json
import pprint
import sys

from .backuptools import BackupTools

config_file = sys.argv[1]
args = sys.argv[2:]

config: dict = None

with open(config_file) as f:
    config = json.load(f)

tools = BackupTools(config)

result = tools.exec(*args)

pprint.pprint(result)
