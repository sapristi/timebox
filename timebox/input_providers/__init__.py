from typing import Union

from .command import CommandInputProvider
from .folder import FolderInputProvider
from .postgres import PostgresInputProvider

InputProvider = Union[FolderInputProvider, PostgresInputProvider, CommandInputProvider]
