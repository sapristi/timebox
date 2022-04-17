import logging
import shlex
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def shlex_join(split_command):
    """Return a shell-escaped string from *split_command*. Python 3.7 compat."""
    return " ".join(shlex.quote(arg) for arg in split_command)


def run_piped_commands(commands: List[List[str]], env, target_file):
    full_command = (
        " | ".join(shlex_join(command) for command in commands)
        + f" > {target_file}"
        + '; printf "${PIPESTATUS[*]}"'
    )
    logger.debug("Running command %s", full_command)
    proc_result = subprocess.Popen(
        full_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        executable="/bin/bash",
    )
    stdout, stderr = proc_result.communicate()
    logger.debug("STDOUT: %s", stdout)
    lines = [l for l in stdout.splitlines() if l]

    return_codes = [int(i) for i in lines[-1].split()]
    if len(return_codes) != len(commands) or set(return_codes) != {0}:
        logger.error(
            """Something wrong happened running '%s':
---
STDOUT: %s
---
STDERR: %s
---
Return codes: %s""",
            full_command,
            stdout,
            stderr,
            return_codes,
        )
    else:
        logger.debug("STDOUT: %s", stdout)
        logger.debug("STDERR: %s", stderr)

    return return_codes
