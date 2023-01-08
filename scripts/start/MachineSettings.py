from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Container
from textual.widgets import Input, Label

class MachineSettings(Widget):

    settings = {
    "machine_name": "test",
    "machine_password": "test123",
    "machine_id": "123",
    "machine_ip": "",
    "machine_cpus": "2",
    "machine_ram": "2048",
    "machine_disk": "10",
    "machine_ssh_port": "22",
    "machine_ssh_key": "~/.ssh/proxmox.pub",
    }

    def compose(self) -> ComposeResult:
        yield Container(
                *[Container(
                    Label(k),
                    Input(placeholder=v, id=k), classes="horizontal-group no-padding") for k,v in self.settings.items()],
                    classes="box"
            )