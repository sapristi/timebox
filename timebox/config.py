from typing import Union

from pydantic import BaseModel

from .input_providers import InputProvider
from .output_providers import OutputProvider
from .rotation_providers import RotationProvider


class ConfigItem(BaseModel):
    name: str
    input: InputProvider
    outputs: list[OutputProvider]
    rotation: RotationProvider

class Config(BaseModel):
    items: list[ConfigItem]

