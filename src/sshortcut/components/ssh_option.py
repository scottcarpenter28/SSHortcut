from textual.app import ComposeResult
from textual.widgets import Button, Label, Static
from textual.containers import Horizontal, Vertical
from textual.message import Message

import atexit
import subprocess

from sshortcut.models.database_connection import DBConnection
from sshortcut.objects.config_storage import SSHConfig
from sshortcut.utils.config import load_or_create_config, Config


def establish_ssh_connection_on_exit(connection: SSHConfig):
    try:
        ssh_command = connection.ssh_connection
        subprocess.Popen(ssh_command, shell=True)
    except Exception as e:
        print(f"Error establishing SSH connection: {e}")


class SSHDisplay(Static):
    def __init__(self, connection: SSHConfig) -> None:
        super().__init__()
        self.server = connection.server
        self.port = str(connection.port)
        self.user = connection.username

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(Label("Server:"), Label(self.server), id="user_server_div"),
            Vertical(Label("Port:"), Label(self.port), id="user_port_div"),
            Vertical(Label("Username:"), Label(self.user), id="username_div"),
        )


class SshOption(Static):

    class ConnectionFileUpdated(Message):
        """Message sent when a new SSH connection is added."""

        pass

    def __init__(self, connection: SSHConfig):
        super().__init__()
        self.connection = connection
        self.config_file: Config = load_or_create_config()
        self.db_conn = DBConnection(
            self.config_file.database.connection, self.config_file.database.echo
        )

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start Connection", id="start", variant="success")
        yield SSHDisplay(connection=self.connection)
        yield Button("Remove", id="remove", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            atexit.register(establish_ssh_connection_on_exit, self.connection)
        elif event.button.id == "remove":
            self.db_conn.delete_ssh_connection(self.connection.id)
            self.post_message(self.ConnectionFileUpdated())
