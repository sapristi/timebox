from functools import reduce
from typing import Any, Dict, Literal, Optional

import requests
from pydantic.fields import Field
from requests.exceptions import HTTPError

from timebox.format_report import FormattedReport

from .base import NotificationProviderBase


def interpolate_body(body, to_replace):
    if isinstance(body, str):
        return reduce(lambda s, kv: s.replace(kv[0], kv[1]), to_replace.items(), body)
    if isinstance(body, list):
        return [interpolate_body(item, to_replace) for item in body]
    if isinstance(body, dict):
        return {k: interpolate_body(v, to_replace) for k, v in body.items()}
    return body


class WebhookNotificationProvider(NotificationProviderBase):
    type: Literal["webhook"]
    method: str
    url: str
    headers: Dict[str, str] = {}
    body: Dict[str, Any] = {}
    secret: Optional[str] = Field(None, secret=True)

    def _send(self, report: FormattedReport):
        if self.secret is not None:
            headers = {k: v.replace("<SECRET>", self.secret) for k, v in self.headers.items()}
            url = self.url.replace("<SECRET>", self.secret)
        else:
            url = self.url
            headers = self.headers

        if self.body:
            body = interpolate_body(
                self.body,
                {
                    "<SUMMARY>": report.summary,
                    "<MESSAGE>": report.message,
                },
            )
            res = requests.request(self.method, url, headers=headers, json=body)
        else:
            res = requests.request(self.method, url, headers=headers)

        try:
            res.raise_for_status()
        except HTTPError:
            self.logger.exception("Failed sending report")
