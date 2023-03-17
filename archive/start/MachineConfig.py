from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, ListItem, ListView, Label, Checkbox
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv, find_dotenv
import os

# load_dotenv('~/Projects/automation2/scripts/.env')
load_dotenv(find_dotenv())

def fetch_machine_images():
    # Returns all images regardless of machine type

    proxmox = ProxmoxAPI(
        os.environ["LOCAL_IP"],
        user=os.environ['USERNAME'],
        backend="ssh_paramiko",
        private_key_file="~/.ssh/proxmox",
    )
    images = proxmox.nodes('bigprox').storage.local.content.get()
    return {
        'lxc': [i["volid"].split("/")[1] for i in images if i['content'] == 'vztmpl'],
        'vm': [i["volid"].split("/")[1] for i in images if i['content'] == 'iso']
    }


class MachineConfig(Widget):
    # provide the initial options from which the reactive state is set and the user can choose from
    options = ["LXC", "VM"]

    # create a reactive value that sets an initial value and is updated according to user input
    machine_type: reactive[str] = reactive(options[0].lower())

    # calculate the image options available
    image_lists = fetch_machine_images()

    image_options = reactive(image_lists['lxc'])

    run_hookscript = reactive(False)

    # create a reactive value that sets an initial value and is updated according to user input
    image: reactive[str | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
            Button("LXC", id="lxc-button-machinetype", classes="button"),
            Button("VM", id="vm-button-machinetype", classes="button"),
            classes="horizontal-group remove",
            id="machinetype_choice_container"
        ),
        Container(ListView(
            *[ListItem(Label(i), id=f"image-{i}") for i in self.image_options],
            id="imagelist",
            classes="",
        ),
        Horizontal(
            Label("Run Hookscript?"),
            Checkbox(value=self.run_hookscript, id="hookscript-checkbox"),
            id="hookscript-container",
            classes="",
        ),
    ),classes="box"
        )

    def watch_machine_type(self, machine_type: str) -> None:
        self.image_options = self.image_lists[machine_type]
    #     # update the buttons to reflect the current value
        for option in self.options:
            self.query_one(f"#{option.lower()}-button-machinetype").remove_class('selected')
        self.query_one(f"#{machine_type}-button-machinetype").add_class('selected')