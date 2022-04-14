import subprocess
from pathlib import Path
from typing import Dict, List, Literal, Optional

from pydantic.fields import Field

from ..common import BackupItem, TempDir, log_failed_command
from .base import InputProviderBase


class CommandInputProvider(InputProviderBase):
    _skip_compress = True

    type: Literal["command"]
    command: List[str]
    extension: Optional[str] = None
    secret: Optional[str] = Field(None, secret=True)
    secret_name: Optional[str] = None
    expected_returncode: Optional[int] = 0
    env_extra: Dict[str, str] = {}

    def _dump(self, tempdir: TempDir, backup_item: BackupItem) -> Path:
        backup_item.extensions.append("tar")
        dest_file = tempdir.get_temp_filepath()
        env = {"DESTFILE": str(dest_file), **self.env_extra}
        if self.secret is not None:
            secret_name = self.secret_name or "SECRET"
            env[secret_name] = self.secret
        res = subprocess.run(self.command, env=env)
        if self.expected_returncode and res.returncode != self.expected_returncode:
            self.logger.error("Execution failed; returncode was %s", res.returncode)
            log_failed_command(self.logger, res, 1000)
        return dest_file

    def __str__(self):
        return f"{self.type}:[{' '.join(self.command)}]"
