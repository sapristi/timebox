import re
from datetime import date, datetime

from pydantic.main import BaseModel

date_format = "%Y%m%d"
filename_regex = r"timebox_(?P<name>.*)_(?P<date>[0-9]{8})\.gz"

class BackupItem(BaseModel):
    name: str
    date: date

    @staticmethod
    def from_filename(filename):
        if match := re.match(filename_regex, filename):
            item_date = datetime.strptime(match.group("date"), date_format).date()
            return BackupItem(name=match.group("name"), date=item_date)
        return None

    @property
    def filename(self):
        return f"timebox_{self.name}_{self.date.strftime(date_format)}.gz"


    @property
    def age(self) -> int:
        return (date.today() - self.date).days

    def __str__(self):
        return f"[{self.name} at {self.date}]"
