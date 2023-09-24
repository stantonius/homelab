# Docker Swarm

**Update**: Docker Swarm does not work within LXC containers. Something to do with the overlay network. So while this script actually works to create a swarm and deploy the portainer instance, we cannot access the portainer web UI because of the overlay network issue.

In order to fix this, we could try:
a) Use a privileged container (although I'm not sure this would even work)
b) Use a VM instead of a container to run the portainer instance

WHile those are easy enough solutions to try, I don't see the huge value in having portainer on my network at the moment as everything I plan to do is with Ansible anyway (meaning creating and destoying will be done with Ansible). So I'm going to leave this as is for now and move on to other things.