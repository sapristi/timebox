from typing import Dict, List, Optional

from pydantic.fields import Field
from typing_extensions import Literal

from ..common import BackupItem
from .base import InputProviderBase


class CommandInputProvider(InputProviderBase):
    """Runs the given command. Use the `DESTFILE` environment variable as the target filename."""

    _skip_compress = True

    type: Literal["command"]
    command: List[str]
    extension: Optional[str] = Field(None, doc_help="Extension to associate with created files.")
    secret: Optional[str] = Field(None, secret=True)
    secret_name: Optional[str] = Field(
        None, doc_help="Environment variable name holding secret value."
    )
    expected_returncode: Optional[int] = 0
    env_extra: Dict[str, str] = Field({}, doc_help="Extra environment variables.")

    def _command(self, backup_item: BackupItem):
        if self.extension:
            backup_item.extensions.append(self.extension)
        env = {**self.env_extra}
        if self.secret is not None:
            secret_name = self.secret_name or "SECRET"
            env[secret_name] = self.secret
        return self.command, env

    def __str__(self):
        return f"{self.type}:[{' '.join(self.command)}]"
