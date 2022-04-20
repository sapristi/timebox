from datetime import date, timedelta
from typing import List, Optional, Union

from typing_extensions import Literal

from timebox.common import BackupItem, BaseModel

from .base import RotationBase


def oldest_item(items):
    return sorted(items, key=lambda i: i.date)[0]


class Day(BaseModel):
    date: date

    def next(self):
        return Day(date=self.date + timedelta(days=1))

    def previous(self):
        return Day(date=self.date - timedelta(days=1))

    def to_interval(self):
        return DateInterval(start=self.date, end=self.next().date)


class Month(BaseModel):
    year: int
    month: int

    def next(self):
        if self.month == 12:
            return Month(year=self.year + 1, month=1)
        else:
            return Month(year=self.year, month=self.month + 1)

    def previous(self):
        if self.month == 1:
            return Month(year=self.year - 1, month=12)
        else:
            return Month(year=self.year, month=self.month - 1)

    def to_date(self):
        return date(year=self.year, month=self.month, day=1)

    def to_interval(self):
        return DateInterval(start=self.to_date(), end=self.next().to_date())


class Year(BaseModel):
    year: int

    def previous(self):
        return Year(year=self.year - 1)

    def next(self):
        return Year(year=self.year + 1)

    def to_date(self):
        return date(year=self.year, month=1, day=1)

    def to_interval(self):
        return DateInterval(start=self.to_date(), end=self.next().to_date())


class DateInterval(BaseModel):
    start: date
    end: date

    def contains(self, day: date):
        return self.start <= day and self.end > day

    def is_after(self, day: date):
        return self.start < day


class PeriodRotation(RotationBase):
    """Ensures oldest backups are kept for each of the given periods.

    For example, if you specify months=2, the oldest of the current month,
    and the oldest of the previous month, will be kept.
    """

    type: Literal["period"]
    days: Optional[int] = None
    months: Optional[int] = None
    years: Optional[int] = None

    def generate_intervals(self, current: Union[Day, Month, Year], nb: Optional[int]):
        if not nb:
            return []
        res = [current.to_interval()]
        for _ in range(nb - 1):
            current = current.previous()
            res.append(current.to_interval())
        return res[::-1]

    def set_remaining_days(self, backup_items: List[BackupItem]) -> List[BackupItem]:
        today = date.today()
        current_year = Year(year=today.year)
        current_month = Month(year=today.year, month=today.month)
        days_intervals = self.generate_intervals(Day(date=today), self.days)
        months_intervals = self.generate_intervals(current_month, self.months)
        years_intervals = self.generate_intervals(current_year, self.years)

        all_intervals = [*days_intervals, *months_intervals, *years_intervals]
        intervals_with_backups = [
            (interval, [item for item in backup_items if interval.contains(item.date)])
            for interval in all_intervals
        ]

        to_keep = {oldest_item(items) for _, items in intervals_with_backups if len(items) > 0}

        return [
            item.copy(update={"remaining_days": None if item in to_keep else 0})
            for item in backup_items
        ]
