import abc
import gzip
import os
import shutil
from pathlib import Path

from ..common import BackupItem, ProviderCommon, TempDir


class InputProviderBase(ProviderCommon, abc.ABC):
    _skip_compress = False

    type: str
    compression: bool = True

    @abc.abstractmethod
    def _dump(self, tempdir: TempDir, backup_item: BackupItem) -> Path:
        pass

    def dump(self, tempdir: TempDir, backup_item: BackupItem) -> Path:
        temp_file_out = self._dump(tempdir, backup_item)
        size = os.path.getsize(temp_file_out)
        self.logger.debug(f"Wrote in %s: %s bytes", temp_file_out, size)
        if not self._skip_compress and self.compression:
            compressed_file_out = self.compress(tempdir, backup_item, temp_file_out)
            os.remove(temp_file_out)
            temp_file_out = compressed_file_out
            size = os.path.getsize(temp_file_out)
            self.logger.debug(f"Wrote in %s: %s bytes", temp_file_out, size)
        return temp_file_out

    def compress(self, tempdir, backup_item: BackupItem, temp_file_in):
        temp_file_out = tempdir.get_temp_filepath()
        self.logger.debug("Compressing with gzip to %s", temp_file_out)
        with open(temp_file_in, "rb") as f_in:
            with gzip.open(temp_file_out, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        backup_item.extensions.append("gzip")
        return temp_file_out
