export ANSIBLE_CONFIG=~/Projects/homelab/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/ansiblepass.txt

# if not in script dir, cd to it
if [ ! -f start.py ]; then
    cd scripts
fi

python start.py