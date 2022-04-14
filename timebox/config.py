import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import validator

from timebox.notification_providers import NotificationProvider

from .common import BaseModel, t
from .input_providers import InputProvider
from .output_providers import OutputProvider
from .rotation_providers import RotationProvider
from .utils import generate_union_parser, generate_union_parser_list

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
    use_secrets: bool = True
    secrets_file: Optional[Path] = None
    notification: Optional[NotificationProvider] = None

    parse_notification = validator("notification", pre=True, allow_reuse=True)(
        generate_union_parser(NotificationProvider)
    )


class Backup(BaseModel):
    name: str
    input: InputProvider
    outputs: list[OutputProvider]
    rotation: RotationProvider

    parse_input = validator("input", pre=True, allow_reuse=True)(
        generate_union_parser(InputProvider)
    )
    parse_outputs = validator("outputs", pre=True, allow_reuse=True)(
        generate_union_parser_list(OutputProvider)
    )


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
