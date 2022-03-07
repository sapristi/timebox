import abc
from pathlib import Path
from typing import Tuple

from timebox.common import BackupItem, ProviderCommon


class OuputProviderBase(ProviderCommon, abc.ABC):
    @abc.abstractmethod
    def _save(self, input_file: Path, backup_item: BackupItem):
        pass

    @abc.abstractmethod
    def _delete(self, backup_item: BackupItem):
        pass

    @abc.abstractmethod
    def _ls_all(self) -> list[Tuple[str, int]]:
        pass

    def already_exists(self, backup_item: BackupItem):
        items = self.ls(backup_item.name)
        return backup_item in items

    def save(self, input_file: Path, backup_item: BackupItem):
        if self.already_exists(backup_item):
            self.logger.warning("Item %s already exists, skipping.", backup_item)
            return
        self._save(input_file, backup_item)
        self.logger.info("[%s] Saved %s", self, backup_item.name)

    def delete(self, backup_item: BackupItem):
        self._delete(backup_item)

    def ls(self, name: str):
        data = self._ls_all()
        items = [BackupItem.from_filename(name, size) for (name, size) in data]
        return [item for item in items if item is not None and item.name == name]
