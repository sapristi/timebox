import abc
import logging
import os
import re
import subprocess
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory, _TemporaryFileWrapper
from typing import Dict, List, Optional, Tuple

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
    extensions: List[str] = pydantic.Field(default_factory=list)
    size: Optional[int] = None

    @staticmethod
    def from_filename(filename, size=None):
        match = re.match(filename_regex, filename)
        if match:
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

    @property
    def size_str(self):
        if self.size is None:
            return "unknown size"
        return f"{format_size(self.size)}"

    def __str__(self):
        return f"[{self.name} on {self.date} ({self.size_str})]"


class ProviderCommon(BaseModel, abc.ABC):
    class Config:
        frozen = False

    @abc.abstractmethod
    def __str__(self):
        pass

    @property
    def logger(self):
        return logging.getLogger(f"timebox.{self}")

    def set_secrets(self, secrets: Dict[str, str]):
        secret_fields = [f for f in self.__fields__.values() if f.field_info.extra.get("secret")]
        for field in secret_fields:
            value = getattr(self, field.name)
            if value is not None:
                if value in os.environ:
                    setattr(self, field.name, os.environ[value])
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


class CompressionAlgo(str, Enum):
    gzip = "gzip"
    bzip2 = "bzip2"
    xz = "xz"

    @property
    def extension(self):
        mapping = {"gzip": "gz", "bzip2": "bz2", "xz": "xz"}
        return mapping[self.value]

    @staticmethod
    def get_doc():
        return "|".join(CompressionAlgo.__members__.values())


def truncate(data, max_len):
    if max_len:
        if len(data) > max_len:
            return data[0:max_len] + "\n....[TRUNCATED]"


def log_failed_command(
    logger, command_res: subprocess.CompletedProcess, max_output_len: Optional[int]
):
    stdout = truncate(command_res.stdout, max_output_len)
    stderr = truncate(command_res.stderr, max_output_len)
    if stdout or stderr:
        logger.error("Captured output:\nSTDOUT: '%s'\nSTDERR: '%s'")
    else:
        logger.error("No outuput.")


class OperationReport(BaseModel):
    items_ok: List[BackupItem]
    items_ko: List[Tuple[BackupItem, List[str]]]
    other_errors: List[str]

    def has_error(self):
        return bool(self.items_ko or self.other_errors)

    def is_empty(self):
        return len(self.items_ok) == 0 and len(self.items_ko) == 0 and len(self.other_errors) == 0


class LsReport(BaseModel):
    items: Dict[str, Dict[str, List[Tuple[BackupItem, int]]]]
    errors: List[str]
