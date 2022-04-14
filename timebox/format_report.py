from timebox.common import OperationReport


def format_operation_report(
    report: OperationReport,
    operation_name,
    operation_verb,
):
    if report.is_empty():
        return f"[{operation_name}]: nothing happened", ""
    summary_list = []
    if len(report.items_ok) > 0:
        summary_list.append(f"{len(report.items_ok)} items {operation_verb}")

    if len(report.items_ko) + len(report.other_errors) > 0:
        summary_list.append(f"{len(report.other_errors) + len(report.items_ko)} errors")
    summary = f"[{operation_name}]: " + ", ".join(summary_list)

    message = f"""{operation_name}:\n"""

    if len(report.items_ok) > 0:
        message += (
            f"- Successfuly {operation_verb} items:\n"
            + "\n".join((f"  + {item}" for item in report.items_ok))
            + "\n"
        )

    if len(report.items_ko) > 0:
        message += "- Items with errors:\n"
        for item, errors in report.items_ko:
            message += f"  + {item}:\n" + "\n".join((f"   * {error}" for error in errors))
        message += "\n"

    return summary, message


class FormattedReport:
    def __init__(self):
        self.summaries = []
        self.messages = []
        self.has_error = False

    @property
    def summary(self):
        preamble = "Warning!" if self.has_error else "All good!"
        return f"[Timebox][{preamble}] {' '.join(self.summaries)}"

    @property
    def message(self):
        return "\n".join(self.messages)

    def add_backup_report(self, report: OperationReport):
        summary, message = format_operation_report(report, "Back-up", "backed-up")
        self.summaries.append(summary)
        self.messages.append(message)
        self.has_error = self.has_error or report.has_error()

    def add_rotate_report(self, report: OperationReport):
        summary, message = format_operation_report(report, "Rotation", "deleted")
        self.summaries.append(summary)
        self.messages.append(message)
        self.has_error = self.has_error or report.has_error()
