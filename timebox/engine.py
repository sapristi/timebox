import logging
from datetime import datetime

import yaml

from timebox.config import Backup, Config

from .common import BackupItem, OperationReport, TempDir
from .format_report import FormattedReport

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
            logger.info("Not using external secrets.")
            return
        if self.config.secrets_file is None:
            logger.debug("Fetching secrets from environment only.")
            secrets = {}
        else:
            logger.debug("Fetching secrets from environment and %s.", self.config.secrets_file)
            with open(self.config.secrets_file) as f:
                secrets = yaml.load(f.read(), Loader=yaml.Loader)

        for backup in self.backups:
            backup.input.set_secrets(secrets)
            for output in backup.outputs:
                output.set_secrets(secrets)

        if self.config.notification is not None:
            self.config.notification.set_secrets(secrets)

    def perform_backups(self) -> OperationReport:
        items_ok = []
        items_ko = []

        for backup in self.backups:
            backup_item = BackupItem(name=backup.name, date=self.date)
            try:
                dump_file = backup.input.dump(self.tempdir, backup_item)
            except Exception as exc:
                message = f"Failed creating dump for {backup_item} ({exc})"
                logger.exception(message)
                items_ko.append((backup_item, [message]))
                continue
            backup_errors = []
            for output in backup.outputs:
                errors = output.save(dump_file, backup_item)
                backup_errors.extend(errors)
            if backup_errors:
                items_ko.append((backup_item, backup_errors))
            else:
                items_ok.append(backup_item)
        return OperationReport(items_ok=items_ok, items_ko=items_ko, other_errors=[])

    def rotate_backups(self) -> OperationReport:
        other_errors = []
        items_ok = []
        items_ko = []
        for backup in self.backups:
            for output in backup.outputs:
                try:
                    output_items = output.ls(backup.name)
                except Exception as exc:
                    message = f"Failed listing backups in {output} ({exc})"
                    logger.exception(message)
                    other_errors.append(message)
                    continue
                for output_item in output_items:
                    if backup.rotation.remaining_days(output_item) == 0:
                        try:
                            output.delete(output_item)
                            items_ok.append(output_item)
                        except Exception as exc:
                            message = (
                                f"Failed deleting backup for {output_item} in {output} ({exc})"
                            )
                            logger.exception(message)
                            items_ko.append((output_item, [message]))
        return OperationReport(items_ok=items_ok, items_ko=items_ko, other_errors=other_errors)

    def run(self):
        backup_report = self.perform_backups()
        rotate_report = self.rotate_backups()

        formatted_report = FormattedReport()
        formatted_report.add_backup_report(backup_report)
        formatted_report.add_rotate_report(rotate_report)

        if self.config.notification:
            self.config.notification.send(formatted_report)

    def ls(self):
        for backup in self.backups:
            for output in backup.outputs:
                try:
                    output_items = output.ls(backup.name)
                except Exception:
                    logger.exception("Failed listing backups in %s", output)
                    continue
                print(f"Items for output {output}")
                for item in output_items:
                    print(f"\t{item}: {backup.rotation.remaining_days(item)} remaining days.")
