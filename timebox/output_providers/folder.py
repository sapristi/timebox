import os
import re
import shutil
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

from .base import OuputProviderBase


class FolderOutputProvider(OuputProviderBase):
    type: Literal["folder"]
    path: Path

    def _save(self, input_file, backup_item):
        dest_name = self.path / backup_item.filename
        shutil.copyfile(input_file.name, dest_name)

    def _ls_all(self):
        return [
            f.name for f in self.path.iterdir()
            if f.is_file()
        ]

    def _delete(self, name):
        os.remove(self.path / name)

    def __str__(self):
        return f"{self.type}:{self.path}"
