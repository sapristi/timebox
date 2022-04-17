from pathlib import Path
from typing import List, Optional

from pydantic import Field
from typing_extensions import Literal

from ..common import BackupItem, CompressionAlgo
from .base import InputProviderBase


class FolderInputProvider(InputProviderBase):
    """Creates a tar archive from a given folder."""

    type: Literal["folder"]
    path: Path = Field(..., doc_help="Path to the folder to compress.")
    compression: Optional[CompressionAlgo] = Field(
        CompressionAlgo.xz, doc_type=CompressionAlgo.get_doc()
    )
    exclude: List[str] = Field(default_factory=list)
    extra_args: List[str] = Field(default_factory=list)

    def _command(self, backup_item: BackupItem):
        backup_item.extensions.append("tar")
        command = ["tar", "-c"]
        for excluded_path in self.exclude:
            command.extend(["--exclude", excluded_path])
        if self.compression:
            command.append(f"--{self.compression.value}")
            backup_item.extensions.append(self.compression.extension)

        command.extend(["-C", str(self.path.parent), self.path.name])
        return command, {}

    def __str__(self):
        return f"{self.type}:{self.path}"
