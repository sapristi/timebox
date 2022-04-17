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
    try:
        return ConfigFile.parse_obj(config_data).parse_backups()
    except Exception as exc:
        print(
            f"{t.red + t.bold}ERROR{t.normal}: Parsing of config file {t.bold}{config_file}{t.normal} failed.\n"
        )
        print(exc)
        exit(1)


def main():
    args = parser.parse_args()

    if args.command == "validate-config":
        config_file = load_config_file(args.config)
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
        ls_report = engine.ls()
        for backup, outputs_data in ls_report.items.items():
            print(f"{t.bold}Backup {backup}:{t.normal}")
            for output, backup_items in outputs_data.items():
                print(f"\t{output}")
                if len(backup_items) == 0:
                    print(f"\t\tNothing here.")
                for (item, remaining_days) in sorted(backup_items, key=lambda i: i[0].age):
                    print(
                        f"\t\t{item.filename}: ({item.age} days old; {remaining_days} remaining days) - {item.size_str}"
                    )


if __name__ == "__main__":
    main()
