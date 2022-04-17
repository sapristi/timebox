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


class PostOp(BaseModel):
    command: List[str] = Field(
        ..., doc_help="Command to run. Should take input from stdin, and output result to stdout."
    )
    extension: str = Field(..., doc_help="Extension to add to the backup files.")


class Config(BaseModel):
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

    post_ops: Dict[str, PostOp] = Field(
        default_factory=dict,
        doc_type="Dict[str, PostOp]",
        doc_help="Definitions for additional commands used to transform the backup (like compression, encryption,...)",
    )

    parse_notification = validator("notification", pre=True, allow_reuse=True)(
        generate_union_parser(NotificationProvider, "NotificationProvider")
    )


from typing import Union

from timebox.input_providers import (
    CommandInputProvider,
    FolderInputProvider,
    PostgresInputProvider,
)


class Backup(BaseModel):
    name: str = Field(
        ...,
        doc_help="Unique name used to identify this backup. Inferred from the `backups` mapping.",
    )
    input: Union[FolderInputProvider, PostgresInputProvider, CommandInputProvider] = Field(
        ..., doc_type="InputProvider"
    )
    outputs: List[OutputProvider] = Field(..., doc_type="List[OutputProvider]")
    rotation: RotationProvider = Field(..., doc_type="RotationProvider")

    parse_input = validator("input", pre=True, allow_reuse=True)(
        generate_union_parser(InputProvider, "InputProvider")
    )
    parse_outputs = validator("outputs", pre=True, allow_reuse=True)(
        generate_union_parser_list(OutputProvider, "OutputProvider")
    )
    parse_rotation = validator("rotation", pre=True, allow_reuse=True)(
        generate_union_parser(RotationProvider, "RotationProvider")
    )
    post_ops: List[str] = Field(default_factory=list, doc_type="List[str]")


class ParsedConfigFile(BaseModel):
    backups: List[Backup]
    config: Config


class ConfigFile(BaseModel):
    backups: Dict[str, Dict]
    config: Config = Field(default_factory=Config)  # type: ignore

    def parse_backups(self):
        backups = []
        for name, backup_dict in self.backups.items():
            try:
                backups.append(Backup(name=name, **backup_dict))
            except Exception:
                print(f"Failed parsing configuration for {t.bold}{name}{t.normal}.")
                raise

        return ParsedConfigFile(config=self.config, backups=backups)
