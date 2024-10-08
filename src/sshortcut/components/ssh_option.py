from textual.app import ComposeResult
from textual.widgets import Button, Label, Static
from textual.containers import Horizontal, Vertical

import atexit
import subprocess

from sshortcut.objects.config_storage import SSHConfig


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
            Vertical(Label("Server:"), Label(self.server), id="user_server_input"),
            Vertical(Label("Port:"), Label(self.port), id="user_port_input"),
            Vertical(Label("Username:"), Label(self.user), id="username_input"),
        )


class SSHOption(Static):

    def __init__(self, connection: SSHConfig):
        super().__init__()
        self.connection = connection

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start Connection", id="start", variant="success")
        yield SSHDisplay(connection=self.connection)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        atexit.register(establish_ssh_connection_on_exit, self.connection)
