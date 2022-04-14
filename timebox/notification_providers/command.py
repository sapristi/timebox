import subprocess
from typing import List, Literal

from timebox.format_report import FormattedReport

from .base import NotificationProviderBase


class CommandNotificationProvider(NotificationProviderBase):
    type: Literal["command"]
    command: List[str]

    def _send(self, report: FormattedReport):
        has_error = "1" if report.has_error else "0"
        env = {
            "SUMMARY": report.summary,
            "MESSAGE": report.message,
            "HAS_ERROR": has_error,
        }
        subprocess.run(self.command, env=env)

    def __str__(self):
        return f"{self.type}:[{' '.join(self.command)}]"
