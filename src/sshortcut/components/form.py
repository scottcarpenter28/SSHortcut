from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Button, Label, Input, Static
from textual.containers import Horizontal, Vertical

from sshortcut.objects.config_storage import ConfigStorage, SSHConfig


class NewSSHForm(Static):

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

        storage_path = Path("./ssh_storage.json")
        if storage_path.exists():
            with open(storage_path, "r") as f:
                current_config = ConfigStorage.model_validate_strings(f.read())
        else:
            current_config = ConfigStorage()

        with open("./ssh_storage.json", "w") as f:
            current_config.options.append(
                SSHConfig(
                    server=server_input.value, port=port, username=user_input.value
                )
            )
            f.write(current_config.model_dump_json())

        server_input.value = ""
        port_input.value = "22"
        user_input.value = ""
