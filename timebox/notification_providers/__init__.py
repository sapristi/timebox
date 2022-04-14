from typing import Union

from timebox.common import BaseModel

from .command import CommandNotificationProvider
from .smtp import SMTPNotificationProvider
from .webhook import WebhookNotificationProvider

NotificationProvider = Union[
    WebhookNotificationProvider, CommandNotificationProvider, SMTPNotificationProvider
]
