# Docker on LXC

I have seen a lot of different perspectives on whether it makes sense to run a container (Docker) inside a container (LXC). However for me, the deciding factor on whether to take this approach was that LXC containers use significantly fewer resources than a VM.

## Docker on boot

Does Docker start on boot? According to [this answer](https://stackoverflow.com/a/67091951), Docker will automatically start on boot after Docker command is run. So our Docker playbook does not need to create a systemd service.