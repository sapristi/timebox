from datetime import date, timedelta

import pytest

from timebox.common import BackupItem
from timebox.rotation_providers import DecayingRotation
from timebox.rotation_providers.decaying_rotation import compute_duration


@pytest.mark.parametrize(
    "start, base",
    (
        (0, 2),
        (0, 3),
        (0, 4),
    ),
)
def test_compute_duration(start, base):
    assert compute_duration(start, base) == 2 ** (base + 1)


@pytest.mark.parametrize(
    "base",
    (
        (2),
        (3),
        (4),
    ),
)
def test_decaying_rotation_day0(base):
    starting_point = date.today()
    rotation = DecayingRotation(
        type="decaying", offset=0, base=base, starting_point=starting_point
    )
    item1 = BackupItem(name="test1", date=date.today())
    assert rotation.remaining_days(item1) == 2 ** (base + 1)


@pytest.mark.parametrize(
    "base",
    (
        (2),
        (3),
        (4),
    ),
)
def test_decaying_rotation_day1(base):
    starting_point = date.today() - timedelta(days=1)
    rotation = DecayingRotation(
        type="decaying", offset=0, base=base, starting_point=starting_point
    )
    item1 = BackupItem(name="test1", date=date.today())
    assert rotation.remaining_days(item1) == 2


@pytest.mark.parametrize(
    "base",
    (
        (3),
        (4),
        (5),
    ),
)
def test_decaying_rotation_day_half(base):
    starting_point = date.today() - timedelta(days=2 ** (base - 1))
    rotation = DecayingRotation(
        type="decaying", offset=0, base=base, starting_point=starting_point
    )
    item1 = BackupItem(name="test1", date=date.today())
    assert rotation.remaining_days(item1) == 2**base
