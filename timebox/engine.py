import logging
from datetime import datetime

import yaml

from .common import BackupItem
from .config import Config, ConfigItem

logger = logging.getLogger(__name__)

def backup(config: Config):
    date = datetime.now().replace(microsecond=0)
    for item in config.items:
        backup_item = BackupItem(name=item.name, date=date)
        backup = item.input.backup(backup_item)
        if backup is None:
            continue
        for output in item.outputs:
            output.save(backup_item, backup)


def rotate(config: Config):
    for config_item in config.items:
        for output in config_item.outputs:
            output_items = output.ls(config_item.name)
            for output_item in output_items:
                if config_item.rotation.remaining_days(output_item) == 0:
                    output.delete(output_item)


def ls(config: Config):
    for config_item in config.items:
        for output in config_item.outputs:
            output_items = output.ls(config_item.name)
            logger.info("Items for output %s", output)
            for item in output_items:
                logger.info("\t%s: %s remaining days.", item, config_item.rotation.remaining_days(item))

def load_config(config_file):
    with open(config_file) as f:
        config_data = yaml.load(f.read(), Loader=yaml.Loader)
    return Config.parse_obj(config_data)
