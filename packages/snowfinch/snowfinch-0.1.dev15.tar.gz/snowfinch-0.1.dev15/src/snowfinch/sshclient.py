import os
from typing import List
from paramiko import AutoAddPolicy, RSAKey, SSHClient
from paramiko import AuthenticationException, SSHException
from scp import SCPClient, SCPException
from snowfinch.logger import log

LOGGER = log.get_logger()


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        ssh_key_filepath: str,
        remote_path: str,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self._upload_ssh_key()

    @property
    def connection(self):
        """Open SSH connection to remote host."""
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                self.host,
                username=self.user,
                password=self.password,
                key_filename=self.ssh_key_filepath,
                timeout=5000,
            )
            return client
        except AuthenticationException as e:
            LOGGER.error(
                f"AuthenticationException occurred; did you remember to generate an SSH key? {e}"
            )
            raise e
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    @property
    def scp(self) -> SCPClient:
        conn = self.connection
        return SCPClient(conn.get_transport())

    def _get_ssh_key(self):
        """Fetch locally stored SSH key."""
        try:
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            LOGGER.info(f"Found SSH key at self {self.ssh_key_filepath}")
            return self.ssh_key
        except SSHException as e:
            LOGGER.error(e)
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    def _upload_ssh_key(self):
        try:
            os.system(
                f"ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1"
            )
            LOGGER.info(f"{self.ssh_key_filepath} uploaded to {self.host}")
        except FileNotFoundError as error:
            LOGGER.error(error)
        except Exception as e:
            LOGGER.error(f"Unexpected error occurred: {e}")
            raise e

    def disconnect(self):
        """Close SSH & SCP connection."""
        if self.connection:
            self.client.close()
        if self.scp:
            self.scp.close()

    def bulk_upload(self, files: List[str]):
        """
        Upload multiple files to a remote directory.
        :param files: List of local files to be uploaded.
        :type files: List[str]
        """
        try:
            self.scp.put(files, remote_path=self.remote_path, recursive=True)
            LOGGER.info(
                f"Finished uploading {len(files)} files to {self.remote_path} on {self.host}"
            )
        except SCPException as e:
            raise e

    def download_file(self, file: str):
        """Download file from remote host."""
        self.scp.get(file)

    def execute_commands(self, commands: List[str]):
        """
        Execute multiple commands in succession.
        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                LOGGER.trace(f"INPUT: {cmd}")
                LOGGER.info(f"OUTPUT: {line}")


def execute_command_on_remote(ssh_remote_client: RemoteClient, commands: List[str] = None):
    """
    Execute UNIX command on the remote host.

    :param ssh_remote_client: Remote server.
    :type ssh_remote_client: RemoteClient
    :param commands: List of commands to run on remote host.
    :type commands: List[str]
    """
    ssh_remote_client.execute_commands(commands)