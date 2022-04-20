import abc
from typing import List

from pydantic import BaseModel

from timebox.common import BackupItem


class RotationBase(BaseModel, abc.ABC):
    type: str

    @abc.abstractmethod
    def set_remaining_days(self, backup_items: List[BackupItem]) -> List[BackupItem]:
        pass
