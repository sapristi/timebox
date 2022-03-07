import abc
import logging
from typing import IO

from pydantic import BaseSettings

from timebox.utils import error_handler

from ..common import BackupItem

logger = logging.getLogger(__name__)


class OuputProviderBase(BaseSettings, abc.ABC):
    name: str = ""
    env_prefix: str = ""
    type: str

    @abc.abstractmethod
    def _save(self, input_file: IO[bytes], backup_item: BackupItem):
        pass

    @abc.abstractmethod
    def _delete(self, backup_item: BackupItem):
        pass

    @abc.abstractmethod
    def _ls_all(self) -> list[str]:
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    def already_exists(self, backup_item: BackupItem):
        items = self.ls(backup_item.name)
        return backup_item in items

    @error_handler(logger, "saving backup")
    def save(self, backup_item: BackupItem, input_file: IO[bytes]):
        if self.already_exists(backup_item):
            logger.warning("Item %s already exists, skipping.", backup_item)
            return
        self._save(input_file, backup_item)
        logger.info("[%s] Saved %s", self, backup_item.name)

    @error_handler(logger, "saving backup")
    def delete(self, backup_item: BackupItem):
        self._delete(backup_item)

    @error_handler(logger, "listing backups")
    def ls(self, name: str):
        names = self._ls_all()
        items = [
            BackupItem.from_filename(name) for name in names
        ]
        return [
            item for item in items
            if item is not None and item.name == name
        ]
