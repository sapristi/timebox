from typing import Union

from .folder import FolderInputProvider
from .postgres import PostgresInputProvider

InputProvider = Union[FolderInputProvider, PostgresInputProvider]
