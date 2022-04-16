from pathlib import Path

import pytest
import yaml

from timebox.config import ConfigFile

config_files_folders = [Path("tests/data/config_files"), Path("config_examples")]
config_files = [
    f
    for config_files_folder in config_files_folders
    for f in config_files_folder.iterdir()
    if f.is_file() and f.suffix in [".yaml", ".yml"]
]


@pytest.mark.parametrize("config_file", config_files)
def test_config_files(config_file):
    with open(config_file) as f:
        f_data = yaml.load(f.read(), Loader=yaml.Loader)
    config_file = ConfigFile.parse_obj(f_data)
    config_file.parse_backups()
    assert isinstance(config_file.config.log_level, str)
