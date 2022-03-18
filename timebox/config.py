import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from .common import BaseModel, t
from .input_providers import InputProvider
from .output_providers import OutputProvider
from .rotation_providers import RotationProvider

logger = logging.getLogger(__name__)


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Config(BaseModel):
    class Config:
        use_enum_values = True

    swallow_errors: bool = True
    log_level: LogLevel = LogLevel.WARNING
    overwrite: bool = False
    secrets_file: Optional[Path] = None


class Backup(BaseModel):
    name: str
    input: InputProvider
    outputs: list[OutputProvider]
    rotation: RotationProvider


class ParsedConfigFile(BaseModel):
    backups: List[Backup]
    config: Config


class ConfigFile(BaseModel):
    backups: Dict[str, Dict]
    config: Config = Config()

    def parse_backups(self):
        backups = []
        for name, backup_dict in self.backups.items():
            try:
                backups.append(Backup(name=name, **backup_dict))
            except Exception:
                print(f"Failed parsing configuration for {t.bold}{name}{t.normal}.")
                raise

        return ParsedConfigFile(config=self.config, backups=backups)
