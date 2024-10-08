import json
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header

from components.ssh_option import SSHOption
from components.form import NewSSHForm
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
                ssh_options.append(SSHOption(connection=option))

        yield ScrollableContainer(NewSSHForm(), *ssh_options, id="ssh_options")

    def action_toggle_dark(self) -> None:
        """
        An action to toggle dark mode.
        """
        self.dark = not self.dark


if __name__ == "__main__":
    app = SSHortcut()
    app.run()
