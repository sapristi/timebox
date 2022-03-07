import tarfile
from pathlib import Path
from typing import Literal

from ..common import BackupItem, TempDir
from .base import InputProviderBase


class FolderInputProvider(InputProviderBase):
    _skip_compress = True

    type: Literal["folder"]
    path: Path

    def _dump(self, tempdir: TempDir, backup_item: BackupItem) -> Path:
        backup_item.extensions.append("tar")
        output = tempdir.get_temp_filepath()
        open_mode = "w"
        if self.compression:
            open_mode += f":gz"
            backup_item.extensions.append("gzip")

        with tarfile.open(name=output, mode=open_mode) as tar:
            tar.add(self.path)

        return output

    def command(self):
        root_dir = str(self.path.name)
        path_to = str(self.path.parent.absolute().resolve())
        return ["/usr/bin/tar", "-C", path_to, "-c", root_dir]

    def __str__(self):
        return f"{self.type}:{self.path}"
