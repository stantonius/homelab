from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv, find_dotenv
import os

# Get env vars from .env file
load_dotenv(find_dotenv())

# Get images from proxmox
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