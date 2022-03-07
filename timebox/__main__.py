import argparse
import logging

from .engine import backup, load_config, ls, rotate

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to config file.")
parser.add_argument("command", choices=["backup", "rotate", "ls", "validate_config"])



if __name__ == "__main__":
    args = parser.parse_args()
    config = load_config(args.config)
    logger = logging.getLogger("timebox")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    if args.command == "rotate":
        rotate(config)
    if args.command == "backup":
        backup(config)
    if args.command == "ls":
        ls(config)

