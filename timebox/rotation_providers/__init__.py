from typing import Union

from .decaying_rotation import DecayingRotation
from .period_rotation import PeriodRotation
from .simple_rotation import SimpleRotation

RotationProvider = Union[SimpleRotation, PeriodRotation, DecayingRotation]
