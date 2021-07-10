
from typing import Any, Dict

FileMeta = Dict[str, Any]


class ParentNotFoundException(Exception):
    def __init__(self, message="Parent not found"):
        self.message = message
        super().__init__(self.message)


class FileNotFoundException(Exception):
    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)


class FileExistedException(Exception):
    def __init__(self, message="File existed"):
        self.message = message
        super().__init__(self.message)
