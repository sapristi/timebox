import tarfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal

from .base import InputProviderBase


class FolderInputProvider(InputProviderBase):
    type: Literal["folder"]
    path: Path

    def _backup(self, backup_item):
        output = NamedTemporaryFile(suffix=backup_item.filename)
        with tarfile.open(fileobj=output, mode="w:gz") as tar:
            tar.add(self.path)
        output.flush()

        return output

    def __str__(self):
        return f"{self.type}:{self.path}"
