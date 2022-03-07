from typing import Union

from .decaying_rotation import DecayingRotation
from .simple_rotation import SimpleRotation

RotationProvider = Union[DecayingRotation, SimpleRotation]
