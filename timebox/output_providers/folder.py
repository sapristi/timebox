import os
import shutil
from pathlib import Path

from typing_extensions import Literal

from ..common import BackupItem
from .base import OuputProviderBase


class FolderOutputProvider(OuputProviderBase):
    """Stores backups in the given local folder."""

    type: Literal["folder"]
    path: Path

    def _save(self, input_file, backup_item):
        dest_name = self.path / backup_item.filename
        shutil.copyfile(input_file, dest_name)

    def _ls_all(self):
        return [
            (f.name, f.stat().st_size)
            for f in self.path.iterdir()
            if f.is_file() and f.name.startswith("timebox")
        ]

    def _delete(self, backup_item: BackupItem):
        os.remove(self.path / backup_item.filename)

    def command(self, backup_item):
        return [str(self.path / backup_item.filename)]

    def __str__(self):
        return f"{self.type}:{self.path}"
