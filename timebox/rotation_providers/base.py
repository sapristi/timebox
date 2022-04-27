import abc
from typing import List, Optional

from pydantic import BaseModel

from timebox.common import BackupItem


class RotationBase(BaseModel, abc.ABC):
    type: str

    @abc.abstractmethod
    def remaining_days(self, backup_item: BackupItem) -> Optional[int]:
        pass

    def set_remaining_days(self, backup_items: List[BackupItem]) -> List[BackupItem]:
        return [
            item.copy(update={"remaining_days": self.remaining_days(item)})
            for item in backup_items
        ]
