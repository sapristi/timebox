from timebox.__main__ import load_config_file
from timebox.engine import Engine


def test_e2e_ok():
    config_file = load_config_file("tests/data/config_files/e2e.yaml")
    engine = Engine(config_file.backups, config_file.config)
    engine.run()
    ls_report = engine.ls()
    assert len(ls_report.items["test"]["folder:/tmp"]) == 1
    assert len(ls_report.errors) == 0
