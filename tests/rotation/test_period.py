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
    assert items_with_remaining_days[0].remaining_days == None
    assert items_with_remaining_days[1].remaining_days == 0


def test_days_month_rotation_1():
    rotation = PeriodRotation(type="period", days=5, months=2)  # type: ignore
    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == None
    assert items_with_remaining_days[1].remaining_days == None


@freeze_time("2010-01-01")
def test_days_month_rotation_2():
    rotation = PeriodRotation(type="period", days=5, months=3)  # type: ignore

    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
        BackupItem(name="test1", date=date.today() - timedelta(days=20)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == None
    assert items_with_remaining_days[1].remaining_days == 0
    assert items_with_remaining_days[2].remaining_days == None


@freeze_time("2010-01-01")
def test_days_month_year_rotation():
    rotation = PeriodRotation(type="period", days=5, months=3, years=2)  # type: ignore

    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
        BackupItem(name="test1", date=date.today() - timedelta(days=20)),
        BackupItem(name="test1", date=date.today() - timedelta(days=150)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == None
    assert items_with_remaining_days[1].remaining_days == 0
    assert items_with_remaining_days[2].remaining_days == None
    assert items_with_remaining_days[3].remaining_days == None


@freeze_time("2010-01-20")
def test_month_rotation():
    rotation = PeriodRotation(type="period", months=1)  # type: ignore

    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
        BackupItem(name="test1", date=date.today() - timedelta(days=10)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == 0
    assert items_with_remaining_days[1].remaining_days == 0
    assert items_with_remaining_days[2].remaining_days == None
