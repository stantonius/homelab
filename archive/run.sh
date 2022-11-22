#!/bin/bash

#########################
# SET DEFAULT VARIABLES #
#########################

node_ssh_key = "~/.ssh/proxmox.pub"
machine_ssh_key = "~/.ssh/proxmox.pub"

#########################
# CHOOSE MACHINE TYPE
#########################

PS3="What do you want to do? "

tasks=($(ls tasks))

select task in "${tasks[@]}" Quit
do
    case $task in
        Quit)
            break
            ;;
        *)
            echo "You chose $task"
            break
            ;;
    esac
done

# echo $REPLY

#######################################
# SELECT THE PROXMOX NODE OR OTHER HOST
#######################################


PS3="On which node do you want to create the $task: "

nodes=("bigprox" "miniprox" "other host")

select node in "${nodes[@]}" Quit
do
    case $REPLY in
        Quit)
            break
            ;;
        *)
            echo "$task in $node"; break;;
    esac
done


#########################
# HELPER FUNCTIONS
#########################

proxmox_machine_config () {
    # prompt the user for the machine name and ensure the name only contains lowercase letters, numbers and dashes
    read -p "Enter the name of the machine: " machine_name
    until [[ $machine_name =~ ^[a-z0-9-]+$ ]]; do
        echo "The machine name can only contain lowercase letters, numbers and dashes. Try again."
        read -p "Enter the name of the machine: " machine_name
    done

    clear

    # prompt the user for the machine id and ensure the id is a number between 100 and 999
    read -p "Enter the VMID of the machine: " machine_id
    until [[ $machine_id =~ ^[1-9][0-9][0-9]$ ]]; do
        echo "The machine id must be a number between 100 and 999. Try again."
        read -p "Enter the VMID of the machine: " machine_id
    done

    clear

    # prompt the user for the machine ip address and ensure the ip address is valid CIDR slash notation
    read -p "Enter the IP address of the machine: " machine_ip
    until [[ $machine_ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; do
        echo "The machine ip address must be valid CIDR notation. Try again."
        read -p "Enter the IP address of the machine: " machine_ip
    done

    clear

    # prompt the user for the machine password and ensure the password
    read -p "Enter the password of the machine: " machine_password
    until [[ $machine_password =~ ^[a-zA-Z0-9!@#$%^\&*()_+]+$ ]]; do
        echo "The machine password must be valid. Try again."
        read -p "Enter the password of the machine: " machine_password
    done

    clear

    # prompt the user for the number of cpus but allow the user to skip this step
    read -p "Enter the number of CPUs for the machine (leave blank for default): " machine_cpus
    until [[ $machine_cpus =~ ^[0-9]+$ ]] || [[ -z $machine_cpus ]]; do
        echo "The number of CPUs must be a number. Try again."
        read -p "Enter the number of CPUs for the machine (leave blank for default): " machine_cpus
    done

    clear

    # prompt the user for the amount of ram but allow the user to skip this step
    read -p "Enter the amount of RAM for the machine (leave blank for default): " machine_ram
    until [[ $machine_ram =~ ^[0-9]+$ ]] || [[ -z $machine_ram ]]; do
        echo "The amount of RAM must be a number. Try again."
        read -p "Enter the amount of RAM for the machine (leave blank for default): " machine_ram
    done

    clear

    # prompt the user for which ssh key location to use but allow the user to skip this step
    read -p "Enter the ssh key location for the Proxmox node (leave blank for proxmox default): " node_ssh_key
    until [[ -f $node_ssh_key ]] || [[ -z $node_ssh_key ]]; do
        echo "The ssh key location must be a valid file. Try again."
        read -p "Enter the ssh key location for the Proxmox node (leave blank for proxmox default): " node_ssh_key
    done

    clear

    # Prompt the user if they want to use
    PS3="Do you want to use a different ssh key for the new virtual machine or container? "
    echo "Note that if using x2go, this key must be RSA"
    ssh_types=("Existing" "New")
    select ssh_type in "${ssh_types[@]}" Quit
    do
        case $ssh_type in
            Quit)
                break
                ;;
            Existing)
                break
                ;;
            New)
                read -p "Enter the location of the ssh file: " ssh_file
                until [[ -f $ssh_file ]]; do
                    echo "The ssh file does not exist. Try again."
                    read -p "Enter the location of the ssh file: " ssh_file
                done
                machine_ssh_key = $ssh_file
                break
                ;;
        esac
    done
}

#########################
# LOGIC TO CREATE MACHINE
#########################

# CREATE LXC
if [[$task == "create_lxc" ]]
then
    proxmox_machine_config

    ansible-playbook -i $node tasks/create_lxc/main.yaml -e "machine_name=$machine_name \
    machine_id=$machine_id machine_ip=$machine_ip machine_password=$machine_password machine_cpus=$machine_cpus \
    machine_ram=$machine_ram machine_disk= node_ssh_key=$node_ssh_key machine_ssh_key=$machine_ssh_key"


# Creating a VM requires us to use Terraform

# if [[ $task == "VM"]]
# then
# awk '/^target_node/{sub(/^target_node.*$/,"target_node = \"test\"")}1' vars.auto.tfvars > vars.auto.tfvars.tmp && mv vars.auto.tfvars.tmp vars.auto.tfvars
# fi

