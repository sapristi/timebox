import smtplib
import ssl
from email.message import EmailMessage
from typing import Literal

from pydantic.fields import Field

from timebox.format_report import FormattedReport

from .base import NotificationProviderBase


class SMTPNotificationProvider(NotificationProviderBase):
    type: Literal["smtp"]
    server: str
    port: int = 465
    sender_email: str
    password: str = Field(..., secret=True)
    dest_email: str

    def _send(self, report: FormattedReport):

        context = ssl.create_default_context()
        msg = EmailMessage()
        msg["Subject"] = report.summary
        msg["From"] = self.sender_email
        msg["To"] = self.dest_email
        msg.set_content(report.message)

        with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.dest_email, msg.as_bytes())
