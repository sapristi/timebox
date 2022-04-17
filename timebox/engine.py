import logging
from datetime import datetime
from typing import List

from dotenv import dotenv_values

from timebox.config import Backup, Config

from .common import BackupItem, LsReport, OperationReport, TempDir
from .format_report import FormattedReport
from .pipe import run_piped_commands

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, backups: List[Backup], config: Config):
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
            secrets = {
                k: v for k, v in dotenv_values(self.config.secrets_file).items() if v is not None
            }

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
                dump_file = self.tempdir.get_temp_filepath()
                command, env = backup.input.get_command(backup_item)
                post_ops = [self.config.post_ops[post_op_name] for post_op_name in backup.post_ops]
                commands = [command, *[post_op.command for post_op in post_ops]]
                backup_item.extensions.extend([post_op.extension for post_op in post_ops])
                run_piped_commands(commands, env, dump_file)
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
        items = {}
        errors = []
        for backup in self.backups:
            items[backup.name] = {}
            for output in backup.outputs:
                try:
                    output_items = output.ls(backup.name)
                except Exception as exc:
                    logger.exception("Failed listing backups in %s", output)
                    errors.append(str(exc))
                    continue
                items[backup.name][str(output)] = [
                    (item, backup.rotation.remaining_days(item)) for item in output_items
                ]
        return LsReport(items=items, errors=errors)
