terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "2.9.11"
    }
  }
}

provider "proxmox" {
  pm_api_url      = var.proxmox_api_url
  pm_tls_insecure = true
  pm_user         = "root@pam"
  pm_password     = var.proxmox_user_pw
}

resource "proxmox_vm_qemu" "cloudinit-test" {
  name        = "tftest1.xyz.com"
  desc        = "tf description"
  target_node = "bigprox"

  iso  = "local:iso/test.iso"
  vmid = 171

  # The destination resource pool for the new VM


  storage = "local-lvm"
  cores   = 3
  sockets = 1
  memory  = 2560
  disk_gb = 4
  nic     = "enp6s0"
  bridge  = "vmbr0"

  ssh_user        = "root"
  ssh_private_key = <<EOF
-----BEGIN RSA PRIVATE KEY-----
private ssh key root
-----END RSA PRIVATE KEY-----
EOF

  os_type = "cloud-init"

  sshkeys = <<EOF
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFPsnf+jir942UpHZFPaQ8C7Gfoo0jmLtdA7wbgnpkw9 craig@MBP.lan
EOF

  provisioner "remote-exec" {
    inline = [
      "ip a"
    ]
  }
}
