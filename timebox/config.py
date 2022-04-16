import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import Field, validator

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

    log_level: LogLevel = Field(
        LogLevel.WARNING.value,
        doc_type="|".join(item for item in LogLevel.__members__),
    )
    secrets_file: Optional[Path] = Field(None, doc_help="Path to a file containing secret values.")
    notification: Optional[NotificationProvider] = Field(
        None,
        doc_type="NotificationProvider",
        doc_help="Specify which provider will be used to send notifications.",
    )
    use_secrets: bool = Field(
        True,
        doc_help="If set to False, secret values should be directly provided in the config file.",
    )

    parse_notification = validator("notification", pre=True, allow_reuse=True)(
        generate_union_parser(NotificationProvider, "NotificationProvider")
    )


class Backup(BaseModel):
    name: str = Field(
        ...,
        doc_help="Unique name used to identify this backup. Inferred from the `backups` mapping.",
    )
    input: InputProvider = Field(..., doc_type="InputProvider")
    outputs: List[OutputProvider] = Field(..., doc_type="List[OutputProvider]")
    rotation: RotationProvider = Field(..., doc_type="RotationProvider")

    parse_input = validator("input", pre=True, allow_reuse=True)(
        generate_union_parser(InputProvider, "InputProvider")
    )
    parse_outputs = validator("outputs", pre=True, allow_reuse=True)(
        generate_union_parser_list(OutputProvider, "OutputProvide")
    )
    parse_rotation = validator("rotation", pre=True, allow_reuse=True)(
        generate_union_parser(RotationProvider, "RotationProvider")
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
