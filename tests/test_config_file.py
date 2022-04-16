from pathlib import Path

import pytest
import yaml

from timebox.config import ConfigFile

example_config_files_folder = Path("tests/data/config_files")
example_config_files = [f for f in example_config_files_folder.iterdir() if f.is_file()]


@pytest.mark.parametrize("config_file", example_config_files)
def test_config_files(config_file):
    with open(config_file) as f:
        f_data = yaml.load(f.read(), Loader=yaml.Loader)
    config_file = ConfigFile.parse_obj(f_data)
    config_file.parse_backups()
    assert isinstance(config_file.config.log_level, str)
