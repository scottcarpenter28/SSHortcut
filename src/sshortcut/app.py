import json
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header

from components.ssh_option import SshOption
from components.form import NewSshForm
from sshortcut.models.database_connection import DBConnection
from sshortcut.objects.config_storage import ConfigStorage, SSHConfig
from sshortcut.utils.config import load_or_create_config, Config


class SSHortcut(App):
    CSS_PATH = "./styles/app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self):
        super().__init__()
        self.config_file: Config = load_or_create_config()
        self.db_conn = DBConnection(
            self.config_file.database.connection, self.config_file.database.echo
        )

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()

        ssh_options = []
        for option in self.db_conn.get_all_ssh_connections():
            ssh_options.append(
                SshOption(
                    connection=SSHConfig(
                        id=option.id,
                        server=option.server,
                        port=option.port,
                        username=option.username,
                    )
                )
            )

        yield ScrollableContainer(NewSshForm(), *ssh_options, id="ssh_options")

    async def on_new_ssh_form_connection_added(
        self, message: NewSshForm.ConnectionAdded
    ) -> None:
        """Handle the custom event triggered when a connection is added."""
        # Reload or refresh the relevant components
        self.refresh_connections()

    async def on_ssh_option_connection_file_updated(
        self, message: SshOption.ConnectionFileUpdated
    ) -> None:
        """Handle the custom event triggered when a connection is added."""
        # Reload or refresh the relevant components
        self.refresh_connections()

    def refresh_connections(self):
        component = self.query_one("#ssh_options")
        ssh_options = self.query("SshOption")
        if ssh_options:
            ssh_options.remove()

        for option in self.db_conn.get_all_ssh_connections():
            component.mount(
                SshOption(
                    connection=SSHConfig(
                        id=option.id,
                        server=option.server,
                        port=option.port,
                        username=option.username,
                    )
                )
            )

    def action_toggle_dark(self) -> None:
        """
        An action to toggle dark mode.
        """
        self.dark = not self.dark


if __name__ == "__main__":
    app = SSHortcut()
    app.run()
