

## Philosophy

Before (ie. in the archive section) I tried to make everything automated and ended up not finishing any of the cool stuff I wanted to do. So I have scraped that approach for now and will use the Proxmox GUI and the tteck proxmox scripts.

I also got too focused on using ansible roles, which I found confusing to split up so much config immediately. So I am now starting with Ansible scripts and will only create roles when it is very obvious it makes sense.

## Environment Variables

* All variables needed in the Caddyfile for example
* Will store them in `/etc/environment`