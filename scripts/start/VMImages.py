from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Static, Checkbox, Label, ListView, ListItem
from textual.reactive import reactive
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv, find_dotenv
import os

# load_dotenv('~/Projects/automation2/scripts/.env')
load_dotenv(find_dotenv())

def fetch_machine_images():
    proxmox = ProxmoxAPI(
        os.environ["LOCAL_IP"],
        user=os.environ['USERNAME'],
        backend="ssh_paramiko",
        private_key_file="~/.ssh/proxmox",
    )
    images = proxmox.nodes('bigprox').storage.local.content.get()
    return [i["volid"].split("/")[1] for i in images if i['content'] == 'vztmpl']

class VMImages(Widget):

    options = fetch_machine_images()

    vm_image: reactive[str] = reactive(options[0])

    def compose(self):
        yield Container(ListView(
            *[ListItem(Label(i), id=f"image-{i}") for i in self.options],
            id="imagelist",
            classes="",
        ))
