from typing import List

from typing_extensions import Literal

from timebox.common import BackupItem

from .base import RotationBase


class SimpleRotation(RotationBase):
    """Keeps backups the given number of days."""

    type: Literal["simple"]
    days: int

    def set_remaining_days(self, backup_items: List[BackupItem]) -> List[BackupItem]:
        return [
            backup_item.copy(update={"remaining_days": self.days - backup_item.age})
            for backup_item in backup_items
        ]
