from datetime import date, datetime, timedelta
from typing import Literal, Optional

from timebox.common import BackupItem

from .base import RotationBase


def compute_duration(start: int, base: int):
    for i in range(base):
        if (start - (2 ** i)) % 2**(i+1) == 0:
            return 2 ** (i+1)
    return 2 ** (base+1)

class DecayingRotation(RotationBase):
    type: Literal["decaying"]
    offset: int = 0
    base: int
    starting_point: date = datetime.fromtimestamp(0).date()

    def remaining_days(self, backup_item: BackupItem)-> float:
        start = (backup_item.date - self.starting_point).days
        retention_days = compute_duration(start, self.base) + self.offset
        return retention_days - backup_item.age
