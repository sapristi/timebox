from datetime import date, timedelta

from timebox.common import BackupItem
from timebox.rotation_providers import SimpleRotation


def test_simple_rotation():
    rotation = SimpleRotation(type="simple", days=5)
    items = [
        BackupItem(name="test1", date=date.today()),
        BackupItem(name="test1", date=date.today() - timedelta(days=5)),
    ]
    items_with_remaining_days = rotation.set_remaining_days(items)
    assert items_with_remaining_days[0].remaining_days == 5
    assert items_with_remaining_days[1].remaining_days == 0
