import tempfile
from datetime import date
from pathlib import Path

from timebox.common import BackupItem
from timebox.output_providers import FolderOutputProvider


def test_folder_output_provider(input_file):
    input_filename, input_size = input_file
    backup_item = BackupItem(name="test", date=date.today(), size=input_size)
    with tempfile.TemporaryDirectory() as tempdir:
        folder_output = FolderOutputProvider(type="folder", path=Path(tempdir))
        folder_output.save(input_filename, backup_item)

        assert folder_output.ls("test")[0] == backup_item

        folder_output.delete(backup_item)
        assert folder_output.ls("test") == []
