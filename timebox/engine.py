import logging
from datetime import datetime

import yaml

from timebox.config import Backup, Config

from .common import BackupItem, TempDir

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, backups: list[Backup], config: Config):
        self.backups = backups
        self.config = config
        self.date = datetime.now().replace(microsecond=0)
        self.provide_secrets()
        self.tempdir = TempDir()

    def provide_secrets(self):
        if not self.config.use_secrets:
            return
        if self.config.secrets_file is None:
            logger.debug("Fetching secrets from environment.")
            secrets = {}
        else:
            logger.debug("Fetching secrets from environment and %s.", self.config.secrets_file)
            with open(self.config.secrets_file) as f:
                secrets = yaml.load(f.read(), Loader=yaml.Loader)

        for backup in self.backups:
            backup.input.set_secrets(secrets)
            for output in backup.outputs:
                output.set_secrets(secrets)

    def create_backups(self):
        for backup in self.backups:
            backup_item = BackupItem(name=backup.name, date=self.date)
            try:
                dump_file = backup.input.dump(self.tempdir, backup_item)
            except Exception as exc:
                logger.error("Failed performing backup dump for %s", backup_item)
                logger.exception(exc)
                continue
            for output in backup.outputs:
                output.save(dump_file, backup_item)

    def rotate_backups(self):
        for backup in self.backups:
            for output in backup.outputs:
                try:
                    output_items = output.ls(backup.name)
                except Exception as exc:
                    logger.error("Failed listing backups in %s", output)
                    logger.exception(exc)
                    continue
                for output_item in output_items:
                    if backup.rotation.remaining_days(output_item) == 0:
                        try:
                            output.delete(output_item)
                        except Exception as exc:
                            logger.error(
                                "Failed deleting backup for %s in %s", output_item, output
                            )
                            logger.exception(exc)

    def run(self):
        self.create_backups()
        self.rotate_backups()

    def ls(self):
        for backup in self.backups:
            for output in backup.outputs:
                try:
                    output_items = output.ls(backup.name)
                except Exception as exc:
                    logger.error("Failed listing backups in %s", output)
                    logger.exception(exc)
                    continue
                print(f"Items for output {output}")
                for item in output_items:
                    print(f"\t{item}: {backup.rotation.remaining_days(item)} remaining days.")
