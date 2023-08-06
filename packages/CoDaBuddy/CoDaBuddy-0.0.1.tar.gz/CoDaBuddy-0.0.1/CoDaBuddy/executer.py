import subprocess
import logging
from Configs import getConfig

from config import DEFAULT

config: DEFAULT = getConfig(config_classes=[DEFAULT])
log = logging.getLogger("databasebackupper")


class Executer:
    def __init__(
        self,
        mode: str,
        container_name: str,
        namespace: str = None,
    ):
        """[summary]

        Args:
            mode (str): ['Docker','kubernetes', 'native'] - Which environment the executer works again
            container_name (str): name/id of the container/pod we will execute the backup on/in
        """
        self.container_name = container_name
        self.mode = mode
        self.namespace = namespace

    def _get_container_exec_command_base(self):
        if self.mode.lower() == "docker":
            return config.DOCKER_COMMAND + " exec"
        elif self.mode.lower() == "kubernetes":
            self.namespace_arg = f"-n {self.namespace if self.namespace else config.KUBECTL_DEFAULT_NAMESPACE}"
            return f"{config.KUBECTL_COMMAND} exec -i {self.namespace_arg}"
        elif self.mode.lower() == "native":
            return ""
        else:
            raise ValueError(
                "Unknown executer mode '{mode}'. Expected on string of ['Docker','kubernetes', 'native']"
            )

    def container_exec(
        self,
        command: str,
        prefix: str = None,
        interactive: bool = False,
        dry_run: bool = False,
    ):
        exec_command = f"{prefix + ' ' if prefix is not None else ''} {self._get_container_exec_command_base()} {'-it' if interactive else ''} {self.container_name}{' --' if self.mode.lower() == 'kubernetes' else ''} {command}"
        if dry_run:
            log.info(
                f"##Dry run!##\nFollowing command will be executed:\n{exec_command}"
            )
            return exec_command
        return self.exec(exec_command)

    @classmethod
    def exec(cls, command: str):
        log.debug(f"Run: `{command}`")
        process = subprocess.Popen(
            config.BASE_EXECUTER_COMMAND + [command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stderr = b""
        stdout = b""
        with process.stderr:
            for line in iter(process.stderr.readline, b""):
                stderr += line
        with process.stdout:
            for line in iter(process.stdout.readline, b""):
                stdout += line

        exitcode = process.wait()

        log.debug(f"Output stdout: {stdout}")
        log.debug(f"Output stderr: {stderr}")
        if stderr or exitcode != 0:
            raise RuntimeError(
                f"""ERROR CODE {exitcode} on command\n'{command}':\n {stderr.decode("utf-8")}"""
            )
        return stdout
