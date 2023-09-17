# Home page will just list all tasks and any notes 

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Static, Input
from textual.containers import Horizontal, Container
from textual.reactive import reactive
from start.CreateVM import CreateVM
from start.CreateLXC import CreateLXC
import json, os, datetime, re, sys
from pathlib import Path
from contextlib import contextmanager
import configparser

# @contextmanager
# def custom_redirection(fileobj):
#     old = sys.stdout
#     sys.stdout = fileobj
#     try:
#         yield fileobj
#     finally:
#         sys.stdout = old

ROOT_DIR = Path('').absolute().parent

config = configparser.ConfigParser(allow_no_value=True, )
config.read(ROOT_DIR/"inventory.ini")

class Home(App):
    CSS_PATH = "./start/start.css"

    state = reactive({
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "task": "",
        "config_file": "",
    })

    def compose(self) -> ComposeResult:
        yield Static("Choose A Task")
        yield Horizontal(
            Button("CreateVM", id="createvm-button-task"),
            Button("CreateLXC", id="createlxc-button-task"),
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "createvm-button-task":
            self.state["task"] = re.sub(r'-button-task', '', event.button.id)
            self.push_screen(CreateVM())
        elif event.button.id == "createlxc-button-task":
            self.state["task"] = re.sub(r'-button-task', '', event.button.id)
            self.push_screen(CreateLXC())
        elif event.button.id == "submit-button":
            self.record()
            self.set_inventory()
            self.run_ansible()

    def set_inventory(self) -> None:
        # we need to create the sections for how we will want to manage these
        # for example, we might want a parent section for all Docker conrainers
        if 'lxc' not in config.sections():
            config.add_section('lxc')
        if 'vm' not in config.sections():
            config.add_section('vm')
        if 'lxc:vars' not in config.sections():
            config.add_section('lxc:vars')
        if 'vm:vars' not in config.sections():
            config.add_section('vm:vars')

        if self.state['task'] == 'createlxc':
            config['lxc:vars']['ansible_user']='stantonius'
            config['lxc:vars']['ansible_ssh_private_key_file']='~/.ssh/proxmox_rsa'
            config['lxc:vars']['ansible_become']='yes'

            lxc_config = self.query_one(CreateLXC).config
            config['lxc'][f"{lxc_config['machine_name']} ansible_host={lxc_config['machine_ip'].split('/')[0]}"]= None

            with open(ROOT_DIR/"inventory.ini", 'w') as configfile:
                config.write(configfile, space_around_delimiters=False)

        if self.state['task'] == 'createvm':
            config['vm:vars']['ansible_user']='stantonius'
            config['vm:vars']['ansible_ssh_private_key_file']='~/.ssh/proxmox_rsa'
            config['vm:vars']['ansible_become']='yes'

            lxc_config = self.query_one(CreateVM).config
            config['vm'][f"{lxc_config['machine_name']} ansible_host={lxc_config['machine_ip'].split('/')[0]}"]= None

            with open(ROOT_DIR/"inventory.ini", 'w') as configfile:
                config.write(configfile, space_around_delimiters=False)
        

    def record(self) -> None:
        self.state['config_file'] = Path(f'{ROOT_DIR.absolute()}/configs/{self.state["task"]}-config-{self.state["date"]}.json')
        # create file if it does not exist
        if not self.state['config_file'].exists():
            self.state['config_file'].touch()
        if self.state['task'] == 'createvm':
            with self.state['config_file'].open('w+') as f:
                json.dump(self.query_one(CreateVM).config, f)
        elif self.state['task'] == 'createlxc':
            with self.state['config_file'].open('w+') as f:
                json.dump(self.query_one(CreateLXC).config, f)
        

    def run_ansible(self) -> None:
        if self.state['task'] == 'createlxc':
            node = self.query_one(CreateLXC).config['node_name']
            os.system(f'ansible-playbook {ROOT_DIR.absolute()}/ansible/playbooks/0_lxc/pm_create_lxc.yaml -e "@{self.state["config_file"]}" -e "node_name={node}"')
            with open(ROOT_DIR/"configs/ansible_command.txt", 'w+') as f:
                f.write(f'ansible-playbook {ROOT_DIR.absolute()}/ansible/playbooks/0_lxc/pm_create_lxc.yaml -e "@{self.state["config_file"]}" -e "node_name={node}"')
        if self.state['task'] == 'createvm':
            node = self.query_one(CreateVM).config['node_name']
            os.system(f'ansible-playbook {ROOT_DIR.absolute()}/ansible/playbooks/0_vm/pm_create_vm_cloud_init.yaml -e "@{self.state["config_file"]}" -e "node_name={node}"')
            with open(ROOT_DIR/"configs/ansible_command.txt", 'w+') as f:
                f.write(f'ansible-playbook {ROOT_DIR.absolute()}/ansible/playbooks/0_vm/pm_create_vm_cloud_init.yaml -e "@{self.state["config_file"]}" -e "node_name={node}"')


if __name__ == "__main__":
    app = Home()
    app.run()
    # with open(ROOT_DIR/"scripts/start.log", 'w+') as out:
    #     with custom_redirection(out):
    #         app.run()