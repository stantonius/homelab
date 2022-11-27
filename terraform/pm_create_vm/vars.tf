# set our vars

variable "proxmox_api_url" {
  type = string
}

variable "proxmox_api_token_id" {
  type      = string
  sensitive = true
}

variable "proxmox_api_token_secret" {
  type      = string
  sensitive = true
}

variable "proxmox_user_pw" {
  type      = string
  sensitive = true
}

# vars for each lxc

# variable "container_name" {
#   type = string
# }

# variable "container_password" {
#   type      = string
#   sensitive = true
# }

# variable "target_node" {
#   type = string
# }

# variable "container_ip" {
#   type = string
# }

# variable "vmid" {
#   type = number
# }
