import abc

from pydantic import BaseModel


class RotationBase(BaseModel, abc.ABC):
    type: str

    @abc.abstractmethod
    def remaining_days(self, backup_item) -> float:
        pass
