import abc
import logging
from typing import IO, Optional

from pydantic import BaseSettings

from timebox.utils import error_handler

from ..common import BackupItem

logger = logging.getLogger(__name__)


class InputProviderBase(BaseSettings, abc.ABC):
    env_prefix: str = ""

    @abc.abstractmethod
    def _backup(self, backup_item: BackupItem) -> IO[bytes]:
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @error_handler(logger, "performing backup")
    def backup(self, backup_item: BackupItem) -> Optional[IO[bytes]]:
        return self._backup(backup_item)
