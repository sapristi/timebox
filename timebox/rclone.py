#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# forked from https://github.com/ddragosd/python-rclone

import json
import logging
import subprocess
import tempfile
from typing import List, Optional

logger = logging.getLogger(__name__)


class RCloneError(Exception):
    def __init__(self, command, stdout, stderr, code):
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.code = code

    def __str__(self):
        return f'rclone failure [{self.code}] for "{self.command}": {self.stderr}'


class RClone:
    """
    Wrapper class for rclone.
    """

    def __init__(self, cfg: Optional[str] = None, executable="rclone"):
        self.cfg = cfg
        self.executable = executable

    def _execute(self, command: List[str]):
        """
        Execute the given `command_with_args` using Popen
        Args:
            - command_with_args (list) : An array with the command to execute,
                                         and its arguments. Each argument is given
                                         as a new element in the list.
        """
        command = [self.executable, *command]
        logger.debug("Invoking : %s", " ".join(command))
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, errors="replace"
        ) as proc:
            (out, err) = proc.communicate()

        logger.debug("Command output: %s", out)
        if proc.returncode != 0:
            raise RCloneError(
                command=" ".join(command), stdout=out, stderr=err, code=proc.returncode
            )

        if err:
            logger.warning(err)

        return out

    def _execute_with_config(self, command: List[str], cfg: str):
        with tempfile.NamedTemporaryFile(mode="w", delete=True) as cfg_file:
            cfg_file.write(cfg)
            cfg_file.flush()

            command_with_config = [*command, "--config", cfg_file.name]
            try:
                command_result = self._execute(command_with_config)
            except Exception:
                raise
            finally:
                cfg_file.close()

        return command_result

    def run_cmd(self, command: str, extra_args: List[str] = []):
        """
        Execute rclone command
        Args:
            - command (string): the rclone command to execute.
            - extra_args (list): extra arguments to be passed to the rclone command
        """
        full_command = [command, *extra_args]
        if self.cfg:
            return self._execute_with_config(full_command, self.cfg)
        else:
            return self._execute(full_command)

    def copy(self, source: str, dest: str, flags=[]):
        """
        Executes: rclone copy source:path dest:path [flags]
        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone copy --help` flags.
        """
        return self.run_cmd(command="copy", extra_args=[source] + [dest] + flags)

    def copyto(self, source: str, dest: str, flags=[]):
        """
        Executes: rclone copyto source:path dest:path [flags]
        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone copy --help` flags.
        """
        return self.run_cmd(command="copyto", extra_args=[source] + [dest] + flags)

    def sync(self, source: str, dest: str, flags=[]):
        """
        Executes: rclone sync source:path dest:path [flags]
        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone sync --help` flags.
        """
        return self.run_cmd(command="sync", extra_args=[source] + [dest] + flags)

    def listremotes(self, flags=[]):
        """
        Executes: rclone listremotes [flags]
        Args:
        - flags (list): Extra flags as per `rclone listremotes --help` flags.
        """
        return self.run_cmd(command="listremotes", extra_args=flags)

    def ls(self, dest: str, flags=[]):
        """
        Executes: rclone ls remote:path [flags]
        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return self.run_cmd(command="ls", extra_args=[dest] + flags)

    def lsjson(self, dest: str, flags=[]):
        """
        Executes: rclone lsjson remote:path [flags]
        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        return json.loads(self.run_cmd(command="lsjson", extra_args=[dest] + flags))

    def delete(self, dest: str, flags=[]):
        """
        Executes: rclone delete remote:path
        Args:
        - dest (string): A string "remote:path" representing the location to delete.
        """
        return self.run_cmd(command="delete", extra_args=[dest] + flags)
