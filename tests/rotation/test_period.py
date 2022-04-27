from datetime import date, timedelta

from freezegun import freeze_time

from timebox.common import BackupItem
from timebox.rotation_providers import PeriodRotation


def test_days_rotation():
    rotation = PeriodRotation(type="period", days=5)  # type: ignore
    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == 5
    assert items_with_remaining_days[1].remaining_days == 0


@freeze_time("2010-01-11")
def test_month_rotation():
    rotation = PeriodRotation(type="period", months=2)  # type: ignore
    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
        BackupItem(name="test1", date=date(year=2010, month=1, day=1)),
        BackupItem(name="test1", date=date(year=2009, month=12, day=1)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == 0
    assert items_with_remaining_days[1].remaining_days == 0
    assert items_with_remaining_days[2].remaining_days == 49
    assert items_with_remaining_days[3].remaining_days == 21


@freeze_time("2010-01-10")
def test_year_rotation():
    rotation = PeriodRotation(type="period", years=2)  # type: ignore

    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date(year=2010, month=1, day=1)),
        BackupItem(name="test1", date=date(year=2009, month=1, day=1)),
        BackupItem(name="test1", date=date(year=2008, month=1, day=1)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == 0
    assert items_with_remaining_days[1].remaining_days == 721
    assert items_with_remaining_days[2].remaining_days == 356
    assert items_with_remaining_days[3].remaining_days == 0
