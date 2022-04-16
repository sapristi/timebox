from pathlib import Path

from typing_extensions import Literal

from ..common import BackupItem
from ..rclone import RClone
from .base import OuputProviderBase

rclone = RClone()


class RCloneOutputProvider(OuputProviderBase):
    """Use rclone to send backups to pre-configured remotes."""

    type: Literal["rclone"]
    executable: str = "rclone"
    remote: str
    path: Path

    @property
    def rclone(self):
        return RClone(executable=self.executable)

    def path_to(self, dest=None):
        if dest is None:
            return f"{self.remote}:{self.path}"
        return f"{self.remote}:{self.path / dest}"

    def _save(self, input_file, backup_item):
        self.rclone.copyto(str(input_file), self.path_to(backup_item.filename))

    def _ls_all(self):
        items = self.rclone.lsjson(self.path_to())
        return [
            (item["Name"], item["Size"])
            for item in items
            if not item["IsDir"] and item["Name"].startswith("timebox")
        ]

    def _delete(self, backup_item: BackupItem):
        self.rclone.delete(self.path_to(backup_item.filename))

    def command(self, backup_item):
        return []

    def __str__(self):
        return f"{self.type}:{self.path_to()}"
