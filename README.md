
## Structure

* The `jobs` directory is the top level dir that contains simple playbooks for automation.
* Anything with the `pm_` prefix is for proxmox

## Setup

* Set the `ANSIBLE_CONFIG` environmental variable to this directory. Can run the `setup.sh` script to do this automatically.

## Design Decisions

* Initially I tried to use a bash script as a "one stop shop" to start each task. However it soon became clear I was managing config in two places and since a) Ansible has prompt functionality and b) I can call Terraform from Ansible, I decided to just use Ansible for all user input.
    * The bash script is in the `archive` directory for future reference.

### Proxmox

I spent way too much time trying to create a one-click solution for creating a VM or container in Proxmox and include setting up all of the config for the machine. This turned out to be difficult for the following reasons:

1. We need to call one machine to create the container/VM, then call another machine to set up the config (the newly created container/VM) - this means we are required to **dynamically set the target hosts** at two different stages of the process, which Ansible doesn't do very well (hosts are loaded statically upon initialization; yes there is the `ansible.builtin.add_host` option). No matter what approach I took, I had to make a compromise. Therefore the final decision is that for Proxmox machines, I will either run manually separate playbooks or combine into one file using two distinct plays. 

2. If you forget to add the `delegate_to` task in every step that requires a different host, you risk running config on the wrong machine.

> If a set of tasks (ie. more than 1-2) require two different hosts, then I will use two different playbooks.


## Tests

Ping all hosts: `ansible all -m ping -v`

## TODO

* Check IP address provided to see if it is used and allow for re-entry if yes. Avoids having to check with router on which IPas are assigned