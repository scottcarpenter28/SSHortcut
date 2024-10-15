import json
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Button, Label, Input, Static
from textual.containers import Horizontal, Vertical
from textual.message import Message

from sshortcut.models.database_connection import DBConnection
from sshortcut.utils.config import Config, load_or_create_config


class NewSshForm(Static):

    class ConnectionAdded(Message):
        """Message sent when a new SSH connection is added."""

        pass

    def __init__(self):
        super().__init__()
        self.config_file: Config = load_or_create_config()
        self.db_conn = DBConnection(
            self.config_file.database.connection, self.config_file.database.echo
        )

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""

        yield Horizontal(
            Vertical(
                Label("Server"),
                Input(placeholder="Server", id="user_server_input"),
                id="user_server_div",
            ),
            Vertical(
                Label("Port"),
                Input(
                    placeholder="22", type="integer", value="22", id="user_port_input"
                ),
                id="user_port_div",
            ),
            Vertical(
                Label("User"),
                Input(placeholder="User", id="user_input"),
                id="username_div",
            ),
            id="form-input",
        )

        yield Button("Add Connection", id="Add", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        server_input = self.query_one("#user_server_input", Input)
        port_input = self.query_one("#user_port_input", Input)
        user_input = self.query_one("#user_input", Input)

        port: int = 22
        if port_input:
            try:
                port = int(port_input.value)
            except ValueError:
                pass

        self.db_conn.add_ssh_connection(
            server=server_input.value, port=port, user=user_input.value
        )

        server_input.value = ""
        port_input.value = "22"
        user_input.value = ""
        self.post_message(self.ConnectionAdded())
