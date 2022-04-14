import argparse
import logging
import sys

import yaml

from .common import t
from .config import ConfigFile
from .engine import Engine

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to config file.")
parser.add_argument("command", choices=["run", "ls", "validate-config"])


def load_config_file(config_file):
    if config_file is None:
        print("{t.red + t.bold}ERROR{t.normal}: No configuration file provided.")
        print("       Use timebox `-c config.yaml` to provide a configuration file.")
        exit(1)
    with open(config_file) as f:
        config_data = yaml.load(f.read(), Loader=yaml.Loader)
    return ConfigFile.parse_obj(config_data).parse_backups()


def main():
    args = parser.parse_args()

    if args.command == "validate-config":
        try:
            config_file = load_config_file(args.config)
        except Exception:
            print(
                f"{t.red + t.bold}ERROR{t.normal}: Parsing of config file {t.bold}{args.config}{t.normal} failed.\n"
            )
            raise
        print(yaml.dump(config_file.dict(), sort_keys=False))
        sys.exit(0)

    config_file = load_config_file(args.config)
    logger = logging.getLogger("timebox")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | [%(name)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(config_file.config.log_level)

    engine = Engine(config_file.backups, config_file.config)
    if args.command == "run":
        engine.run()
    if args.command == "ls":
        engine.ls()


if __name__ == "__main__":
    main()
