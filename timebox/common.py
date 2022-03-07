import abc
import logging
import re
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory, _TemporaryFileWrapper
from typing import Optional

import pydantic
from blessings import Terminal

from .utils import format_size

t = Terminal()
Tempfile = _TemporaryFileWrapper
date_format = "%Y%m%d"
filename_regex = r"timebox_(?P<name>.*)_(?P<date>[0-9]{8})(?P<extensions>([a-z0-9.])*)"


class BaseModel(pydantic.BaseModel):
    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class BackupItem(BaseModel):
    name: str
    date: date
    extensions: list[str] = []
    size: Optional[int] = None

    @staticmethod
    def from_filename(filename, size=None):
        if match := re.match(filename_regex, filename):
            item_date = datetime.strptime(match.group("date"), date_format).date()
            extensions = [ext for ext in match.group("extensions").split(".") if ext]
            return BackupItem(
                name=match.group("name"), date=item_date, extensions=extensions, size=size
            )
        return None

    @property
    def filename(self):
        return f"timebox_{self.name}_{self.date.strftime(date_format)}.{'.'.join(self.extensions)}"

    @property
    def age(self) -> int:
        return (date.today() - self.date).days

    def __str__(self):
        if self.size is None:
            size_str = ""
        else:
            size_str = f" ({format_size(self.size)})"
        return f"[{self.name} at {self.date}{size_str}]"


class ProviderCommon(BaseModel, abc.ABC):
    class Config:
        frozen = False

    @abc.abstractmethod
    def __str__(self):
        pass

    @property
    def logger(self):
        return logging.getLogger(f"timebox.{self}")

    def set_secrets(self, secrets: dict[str, str]):
        secret_fields = [f for f in self.__fields__.values() if f.field_info.extra.get("secret")]
        for field in secret_fields:
            value = getattr(self, field.name)
            if value is not None:
                if value in secrets:
                    setattr(self, field.name, secrets[value])
                else:
                    raise ValueError(f"No secret found for {self}.{field.name}")


class TempDir:
    def __init__(self):
        self.tempdir = TemporaryDirectory(prefix="timebox")

    def get_temp_filepath(self):
        unique_token = str(datetime.now().timestamp())
        return Path(self.tempdir.name) / unique_token

    def cleanup(self):
        self.tempdir.cleanup()


# unused for now
class Compression(str, Enum):
    gzip = "gzip"
    bzip2 = "bzip2"
    lzma = "lzma"

    @property
    def extension(self):
        mapping = {"gzip": "gz", "bzip2": "bz2", "lzma": "xz"}
        return mapping[self.value]
