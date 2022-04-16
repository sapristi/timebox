import subprocess
from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from ..common import BackupItem, TempDir
from .base import InputProviderBase


class PostgresInputProvider(InputProviderBase):
    """Dumps the given postgres database."""

    type: Literal["postgres"]
    database: str
    host: Optional[str] = None
    username: Optional[str] = None
    port: Optional[str] = None
    password: Optional[str] = Field(secret=True)
    executable: str = "/usr/bin/pg_dump"

    def _dump(self, tempdir: TempDir, backup_item: BackupItem):
        output = tempdir.get_temp_filepath()
        cmd, env = self.command(file=str(output))
        subprocess.run(cmd, env=env, check=True)
        backup_item.extensions.append("sql")
        return output

    def command(self, file=None):
        cmd = [self.executable, "--no-password"]
        if self.username is not None:
            cmd.extend(["-U", self.username])
        if self.host is not None:
            cmd.extend(["-h", self.host])
        if self.port is not None:
            cmd.extend(["-p", self.port])

        if file is not None:
            cmd.extend(["--file", file])

        cmd.append(self.database)
        env = {}
        if self.password is not None:
            env["PGPASSWORD"] = self.password

        return cmd, env

    def __str__(self):
        return f"{self.type}:{self.database}"
