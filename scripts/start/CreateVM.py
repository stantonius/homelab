from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Static, Input, ListView, ListItem, Label
from textual.containers import Horizontal, Container
from textual.reactive import reactive
from textual import events
from textual.events import InputEvent
from rich.pretty import pprint, Pretty
from rich.panel import Panel
from pathlib import Path
from .images import fetch_machine_images

ROOT_DIR = Path('').absolute().parent.parent

# Get images from proxmox
images = fetch_machine_images()


# List of settings we need 
settings = {
    "task_description": "",
    "node_name": "",
    "machine_name": "",
    "machine_user": "stantonius",
    "machine_password": "",
    "machine_image": "",
    "machine_id": "",
    "machine_ip": "",
    "machine_cpus": "2",
    "machine_cores": "2",
    "machine_ram": "2048",
    "machine_disk": "10",
    "machine_ssh_port": "22",
    "machine_ssh_key": "~/.ssh/proxmox_rsa.pub",
}

def create_option(name: str, value: str) -> Widget:
    # NOTE: The name is very important and should be exactly the same as the key in the config dict
    # this name is used as the id below and will update the config dict
    # value should be empty string if not set

    return Horizontal(
        Static(name, id=f"option-text-{name}", classes="option-text"),
        Input(value=value, id=f"option-config-{name}", classes="option-input"),
        classes="cols"
    )


class CreateVM(Screen):

    config: reactive[dict] = reactive(settings, layout=True)

    def compose(self) -> ComposeResult:
        yield Container(
                Static("Config Settings"),
                Static(Pretty(self.config, expand_all=True), id="test"), id="sidebar"
            )
        yield Container(
        Static("Create VM"),
        Horizontal(
            Static("Choose Node:", id="node-header-text"),
            Button("Bigprox", id="bigprox-node-button"),
            Button("Miniprox", id="miniprox-node-button"),
            classes="cols",
        ),
        Horizontal(
            Static("machine_image"),
            ListView(
            *[ListItem(Label(i), id=f"image-{i}") for i in images['vm']],
            id="imagelist",
            
            ),
            classes="cols",
        ),
        Container(
            *[create_option(name, value) for name, value in settings.items() if name not in ["machine_image", 'node_name']],
            classes="cols",
        ),
        Button(
            "Submit",
            id="submit-button",
        ),
        id="mainbar"
        )

    def on_mount(self) -> None:
        previous_configs = [f for f in (ROOT_DIR/"configs").glob("*") if "createvm" in f.name]
        # TODO: load in previous config. Might need to be when class is initialized and not on mount


    def on_input_changed(self, event: Input.Changed) -> None:
        # remove the option-config- from the id
        # then update the config dict with the new value
        self.config[event.input.id[14:]] = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if "-node-button" in event.button.id:
            self.config["node_name"] = event.button.id.split("-")[0]
            self.query_one(f"#{event.button.id}").add_class("selected")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.config['machine_image'] = event.item.id[len('image-'):]