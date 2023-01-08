from textual.app import App, ComposeResult
from textual import events
from textual.containers import Container, Vertical
from textual.widgets import Button, Header, Footer, Static, Checkbox, ListView, ListItem, Label, Placeholder, Input
from start.Options import Options
from start.Tasks import Tasks
from start.Nodes import Nodes
from start.VMImages import VMImages
from start.MachineType import MachineType
from start.MachineConfig import MachineConfig
from start.MachineSettings import MachineSettings
from textual import events, log
import json, os

# initialize the Ansible env vars
os.environ["ANSIBLE_CONFIG"]="~/Projects/automation2/ansible.cfg"
os.environ["ANSIBLE_VAULT_PASSWORD_FILE"]="~/ansiblepass.txt"

class Homelab(App):
    CSS_PATH = "./start/main.css"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("escape", "app.pop_screen", "Pop screen")
    ]

    settings = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Options()
        yield MachineConfig()
        yield MachineSettings()
        yield Button("Complete", id="complete", classes="button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if "-task" in  event.button.id:
            option_selected = event.button.id.split("-")[0]
            self.query_one(Tasks).task = option_selected
            # self.query_one("#task_choice_label", Static).update(self.query_one(Tasks).task)
            self.query_one("#node_choice_container").styles.display = "block" if option_selected == 'proxmox' else "none"
        if "-node" in  event.button.id:
            option_selected = event.button.id.split("-")[0]
            self.query_one(Nodes).node = option_selected
        if "-machinetype" in  event.button.id:
            option_selected = event.button.id.split("-")[0]
            self.query_one(MachineType).machine_type = option_selected
        if event.button.id == "complete":
            self.action_complete()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.sender.id == 'imagelist':
            self.query_one(VMImages).vm_image = event.item.id.replace("image-", "")

    def on_input_changed(self, event: Input.Changed) -> None:
        # will need to specify which input changed if we ever add more
        self.query_one(MachineSettings).settings[event.input.id] = event.value

    def record(self) -> None:
        # write the settings dictioonary to a json file called config.json
        with open('config.json', 'w') as f:
            json.dump(self.settings, f)
        

    def run_ansible(self) -> None:
        if self.settings['type'] == 'lxc':
            node = self.settings['node']
            os.system(f'ansible-playbook ansible/playbooks/pm_create_lxc.yaml --extra-vars "node_name={node}"')
        if self.settings['type'] == 'vm':
            os.system(f'ansible-playbook ../ansible/playbooks/pm_create_vm.yaml')

    def action_complete(self) -> None:
        self.settings['task'] = self.query_one(Tasks).task
        self.settings['node'] = self.query_one(Nodes).node
        self.settings['type'] = self.query_one(MachineType).machine_type
        self.settings['machine_image'] = self.query_one(VMImages).vm_image
        self.settings.update(self.query_one(MachineSettings).settings)
        print(self.settings)
        self.record()
        self.run_ansible()


if __name__ == "__main__":
    app = Homelab()
    app.run()
