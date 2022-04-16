from timebox.__main__ import load_config_file
from timebox.engine import Engine


def test_provide_secrets():
    config_file = load_config_file("tests/data/config_files/test_secrets.yaml")
    engine = Engine(config_file.backups, config_file.config)

    assert engine.backups[0].input.password == "my_db_pwd"
    assert engine.config.notification.secret == "dontsharewithanyone"
