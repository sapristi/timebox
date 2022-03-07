import abc
from datetime import date, timedelta

from pydantic import BaseModel

from timebox.common import BackupItem


class RotationBase(BaseModel, abc.ABC):
    type: str

    @abc.abstractmethod
    def remaining_days(self, backup_item) -> float:
        pass
