terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "2.9.11"
    }
  }
}



# set our provider

# cannot use this method if we want to use ssh or provide a hookscript
# provider "proxmox" {
#   pm_api_url      = var.proxmox_api_url
#   pm_tls_insecure = true
#   pm_api_token_id     = var.proxmox_api_token_id
#   pm_api_token_secret = var.proxmox_api_token_secret
# }

provider "proxmox" {
  pm_api_url      = var.proxmox_api_url
  pm_tls_insecure = true
  pm_user         = "root@pam"
  pm_password     = var.proxmox_user_pw
}

# create our container

resource "proxmox_lxc" "lxc" {
  target_node  = var.target_node
  hostname     = var.container_name
  ostemplate   = "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
  password     = var.container_password
  unprivileged = true

  rootfs {
    storage = "local-lvm"
    size    = "8G"
  }

  network {
    name   = "enp6s0"
    bridge = "vmbr0"
    ip     = var.container_ip
  }

  ssh_public_keys = file("~/.ssh/proxmox.pub")

  memory = 2048
  vmid   = var.vmid
  start  = true
  onboot = false

  # hookscript = "local:snippets/enable_lxc_ssh_hook.sh"

  # can also set more advanced options via cloud-init
  # see near the end of this vid https://youtu.be/dvyeoDBUtsU
  # Note: Not sure if this works for LXC actually
  # os_type = "cloud-init"
  # ipconfig0 = "ip=192.168.1.81/24,gw=192.168.1.1"
  # nameserver = "10.0.0.1"
  # sshkeys
  # user

}
