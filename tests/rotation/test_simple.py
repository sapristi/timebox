from datetime import date, timedelta

from timebox.common import BackupItem
from timebox.rotation_providers import SimpleRotation


def test_simple_rotation():
    rotation = SimpleRotation(type="simple", days=5)
    item1 = BackupItem(name="test1", date=date.today())
    assert rotation.remaining_days(item1) == 5

    item2 = BackupItem(name="test1", date=date.today() - timedelta(days=5))
    assert rotation.remaining_days(item2) == 0
