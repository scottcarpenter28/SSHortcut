import json
from pathlib import Path
from typing import Union

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header

from components.ssh_option import SshOption
from components.form import NewSshForm
from sshortcut.objects.config_storage import ConfigStorage


class SSHortcut(App):
    CSS_PATH = "./styles/app.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()

        storage_path = Path("./ssh_storage.json")
        ssh_options = []
        if storage_path.exists():
            with storage_path.open("r") as f:
                data = json.loads(f.read())
                config_values = ConfigStorage(**data)

            for option in config_values.options:
                ssh_options.append(SshOption(connection=option))

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

        storage_path = Path("./ssh_storage.json")
        if storage_path.exists():
            with storage_path.open("r") as f:
                data = json.loads(f.read())
                config_values = ConfigStorage(**data)

            for option in config_values.options:
                component.mount(SshOption(connection=option))

    def action_toggle_dark(self) -> None:
        """
        An action to toggle dark mode.
        """
        self.dark = not self.dark


if __name__ == "__main__":
    app = SSHortcut()
    app.run()
