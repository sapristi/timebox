from datetime import date

from typing_extensions import Literal

from timebox.common import BackupItem, BaseModel

from .base import RotationBase


class Month(BaseModel):
    year: int
    month: int

    def next(self, nb=1):
        if self.month == 12:
            next_month = Month(year=self.year + 1, month=1)
        else:
            next_month = Month(year=self.year, month=self.month + 1)
        if nb == 1:
            return next_month
        else:
            return next_month.next(nb=nb - 1)

    @staticmethod
    def from_date(d: date):
        return Month(year=d.year, month=d.month)

    def to_date(self):
        return date(year=self.year, month=self.month, day=1)


class PeriodRotation(RotationBase):
    """Ensures backups are kept for each of the given periods.

    For example, if you specify months=2, the backups made
    on the first day of a month will be kept for 2 months.
    """

    type: Literal["period"]
    days: int = 0
    months: int = 0
    years: int = 0

    def remaining_days_for_days(self, backup_item: BackupItem) -> int:
        if self.days == 0:
            return 0
        return self.days - backup_item.age

    def remaining_days_for_months(self, backup_item: BackupItem) -> int:
        if self.months == 0:
            return 0
        if not backup_item.date.day == 1:
            return 0
        end_month = Month.from_date(backup_item.date).next(nb=self.months)
        end_date = end_month.to_date()
        print(f"END DAte for {backup_item.date} is", end_date)
        return (end_date - date.today()).days

    def remaining_days_for_years(self, backup_item: BackupItem) -> int:
        if self.years == 0:
            return 0
        if not (backup_item.date.day == 1 and backup_item.date.month == 1):
            return 0
        end_year = backup_item.date.year + self.years
        end_date = date(year=end_year, month=1, day=1)
        return (end_date - date.today()).days

    def remaining_days(self, backup_item: BackupItem) -> int:
        return max(
            self.remaining_days_for_days(backup_item),
            self.remaining_days_for_months(backup_item),
            self.remaining_days_for_years(backup_item),
        )
