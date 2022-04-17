from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from .base import InputProviderBase


class PostgresInputProvider(InputProviderBase):
    """Dumps the given postgres database."""

    type: Literal["postgres"]
    database: str
    host: Optional[str] = None
    username: Optional[str] = None
    port: Optional[str] = None
    password: Optional[str] = Field(secret=True)

    def _command(self, backup_item):
        cmd = ["pg_dump", "--no-password"]
        if self.username is not None:
            cmd.extend(["-U", self.username])
        if self.host is not None:
            cmd.extend(["-h", self.host])
        if self.port is not None:
            cmd.extend(["-p", self.port])

        cmd.append(self.database)
        env = {}
        if self.password is not None:
            env["PGPASSWORD"] = self.password

        return cmd, env

    def __str__(self):
        return f"{self.type}:{self.database}"
