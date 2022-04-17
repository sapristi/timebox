import abc
from typing import Dict, List, Tuple

from ..common import BackupItem, ProviderCommon


class InputProviderBase(ProviderCommon, abc.ABC):
    type: str

    @abc.abstractmethod
    def _command(self, backup_item: BackupItem) -> Tuple[List[str], Dict[str, str]]:
        pass

    def get_command(self, backup_item) -> Tuple[List[str], Dict[str, str]]:
        return self._command(backup_item)
