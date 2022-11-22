import configparser
import re
import os
import json

def task_type():
    tasks = ['proxmox', 'other']
    while True:
        print(f'Select task type from options {tasks}. Press Enter to use default [proxmox]:')
        task = input()
        if task == '':
            print("Selected proxmox \n")
            return 'proxmox'
        if task in tasks:
            print("Selected " + task + " \n")
            return task
        else:
            print('Invalid task type. Must be one of: {}'.format(tasks))

def node_name():
    nodes = ["bigprox", "miniprox"]
    while True:
        print(f'Select node name from options {nodes}. Press Enter to use default [bigprox]:')
        node = input()
        if node == '':
            print("Selected bigprox \n")
            return 'bigprox'
        if node in nodes:
            print("Selected " + node + " \n")
            return node
        else:
            print('Invalid node name. Must be one of: {}'.format(nodes))

def machine_type():
    machines = ["container", "vm"]
    while True:
        print(f'Select machine type from options {machines}. Press Enter to use default [container]:')
        machine = input()
        if machine == '':
            print("Selected container \n")
            return 'container'
        if machine in machines:
            print("Selected " + machine + " \n")
            return machine
        else:
            print('Invalid machine type. Must be one of: {}'.format(machines))

def machine_name():
    while True:
        print('Enter machine name:')
        name = input()
        if name == '':
            print('Machine name cannot be blank.')
        else:
            print('Machine name is ' + name + '\n')
            return name

def machine_password():
    while True:
        print('Enter machine password:')
        password = input()
        if password == '':
            print('Machine password cannot be blank.')
        else:
            print('Machine password set \n')
            return password

def machine_id():
    while True:
        print('Enter machine id:')
        id = input()
        if id == '':
            print('Machine id cannot be blank.')
        elif not id.isnumeric():
            print('Machine id must be numeric.')
        elif int(id) < 100 or int(id) > 999:
            print('Machine id must be 3 digits between 100 and 999.')
        else:
            print('Machine id is ' + id + '\n')
            return id

def machine_ip():
    while True:
        print('Enter machine ip:')
        ip = input()
        if ip == '':
            print('Machine ip cannot be blank.')
        # create elif condition that users regex to validate CIDR ip address
        elif not re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', ip):
            print('Machine ip must be in CIDR format.')
        else:
            print('Machine ip is ' + ip + '\n')
            return ip

def machine_cpus():
    while True:
        print('Enter number of cpus. Press Enter to use default [2]:')
        cpus = input()
        if cpus == '':
            print("Selected 2 CPUs \n")
            return 2
        elif not cpus.isnumeric():
            print('Machine cpus must be numeric.')
        elif int(cpus) < 1 or int(cpus) > 16:
            print('Machine cpus must be between 1 and 16.')
        else:
            print("Selected " + cpus + " CPUs \n")
            return cpus

def machine_cores():
    while True:
        print('Enter number of cores. Press Enter to use default [2]:')
        cores = input()
        if cores == '':
            print("Selected 2 cores \n")
            return 2
        elif not cores.isnumeric():
            print('Machine cores must be numeric.')
        elif int(cores) < 1 or int(cores) > 16:
            print('Machine cores must be between 1 and 16.')
        else:
            print("Selected " + cores + " cores \n")
            return cores

def machine_ram():
    while True:
        print('Enter the amount of ram. Press Enter to use default [2048]:')
        ram = input()
        if ram == '':
            print("Selected 2048 MB of ram \n")
            return 2048
        elif not ram.isnumeric():
            print('Machine ram must be numeric.')
        elif int(ram) < 512 or int(ram) > 65536:
            print('Machine ram must be between 512 and 65536.')
        else:
            print("Selected " + ram + " MB of ram \n")
            return ram

def machine_disk():
    while True:
        print('Enter the amount of disk space. Press Enter to use default [16]:')
        disk = input()
        if disk == '':
            print("Selected 16 GB of disk space \n")
            return 16
        elif not disk.isnumeric():
            print('Machine disk space must be numeric.')
        elif int(disk) < 1 or int(disk) > 1000:
            print('Machine disk space must be between 1 and 1000.')
        else:
            print("Selected " + disk + " GB of disk space \n")
            return disk

def machine_image(machine_type: str):
    # Borrowed from https://bobbyhadz.com/blog/python-select-option-input

    config = configparser.ConfigParser(allow_no_value=True)
    config.read("images.ini")
    images = [im for im in config[machine_type]]

    user_input = ''

    input_message = 'Select image. Press Enter to use default [{}]: \n'.format(images[0])
    for index, item in enumerate(images):
        input_message += f'{index+1}) {item}\n'

    input_message += 'Your choice: '

    while user_input not in map(str, range(1, len(images) + 1)):
        print(f"Must select a number between 1 and {len(images)}")
        user_input = input(input_message)

    image_selected = images[int(user_input) - 1]
    print('You picked: ' + image_selected)
    return image_selected

def ssh_port():
    while True:
        print('Enter ssh port. Press Enter to use default [22]:')
        port = input()
        if port == '':
            return 22
        elif not port.isnumeric():
            print('Machine ssh port must be numeric.')
        elif port < 1 or port > 65535:
            print('Machine ssh port must be between 1 and 65535.')
        else:
            return port

def ssh_key(key_type: str = "~/.ssh/proxmox.pub"):
    while True:
        print(f'Enter ssh key. Press Enter to use default [{key_type}]:')
        key = input()
        if key == '':
            print("Selected default key \n")
            return key_type
        elif not os.path.isfile(key):
            print('File does not exist.')
        else:
            print("Selected " + key + " \n")
            return key


def config():
    # call all functions and store results in a dictionary
    machine = {}
    machine["task_type"] = task_type()
    machine['machine_type'] = machine_type()
    if machine["task_type"] == "proxmox":
        machine["node_name"] = node_name()
    machine['machine_name'] = machine_name()
    machine['machine_password'] = machine_password()
    machine['machine_id'] = machine_id()
    machine['machine_ip'] = machine_ip()
    machine['machine_cpus'] = machine_cpus()
    machine['machine_cores'] = machine_cores()
    machine['machine_ram'] = machine_ram()
    machine['machine_disk'] = machine_disk()
    machine['machine_image'] = machine_image(machine['machine_type'])
    machine['ssh_port'] = ssh_port()
    machine['machine_ssh_key'] = ssh_key()

    return machine

def main():
    # Here is where we call the different Ansible playbooks or Terraform modules
    machine_config = config()

    # save config as ansible_config.json in the /tmp directory
    with open('/tmp/ansible_config.json', 'w') as outfile:
        json.dump(machine_config, outfile)


    if machine_config['task_type'] == 'proxmox':
        if machine_config['machine_type'] == 'container':
            # call ansible playbook for proxmox container
            os.system(f'ansible-playbook ansible/playbooks/pm_create_lxc.yaml --extra-vars "@{outfile.name}"')
        elif machine_config['machine_type'] == 'vm':
            # call ansible playbook for proxmox vm
            os.system(f'ansible-playbook ansible/playbooks/pm_create_vm.yaml --extra-vars "@{outfile.name}"')


if __name__ == '__main__':
    main()