from typing import Union

from .folder import FolderOutputProvider
from .rclone import RCloneOutputProvider

OutputProvider = Union[FolderOutputProvider, RCloneOutputProvider]
