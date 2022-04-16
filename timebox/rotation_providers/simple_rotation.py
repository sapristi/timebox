from typing_extensions import Literal

from timebox.common import BackupItem

from .base import RotationBase


class SimpleRotation(RotationBase):
    """Keeps backups the given number of days."""

    type: Literal["simple"]
    days: int

    def remaining_days(self, backup_item: BackupItem) -> int:
        return self.days - backup_item.age
