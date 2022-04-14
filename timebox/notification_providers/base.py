import abc

from timebox.common import ProviderCommon
from timebox.format_report import FormattedReport


class NotificationProviderBase(ProviderCommon, abc.ABC):
    type: str

    @abc.abstractmethod
    def _send(self, report: FormattedReport):
        pass

    def send(self, report: FormattedReport):
        self._send(report)

    def __str__(self):
        return f"{self.type}"
