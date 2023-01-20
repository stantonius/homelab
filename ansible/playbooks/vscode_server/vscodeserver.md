# Hosting a VSCode Server on my Homelab

## Configuration Notes

* Created a systemd service so that even if the container or server goes offline, the vscode server should restart.

## Manual setup

Despite my deep desire to automate everything, the one part we have to do manually is 

The steps are:
1. Run the command `./code tunnel` to initialize the tunnel.
2. Accept the terms and sign into Github.
3. Create a name for the machine. In my case I called the machine `homecode`.
4. Open the URL that is generated at the domain `vscode.dev`

In my case, the generated URL is: `https://vscode.dev/tunnel/homecode`


Note that once the tunnel is running, it stays open until the the host machine disconnects (ie. goes offline). So given that we are running this in our home server, we should always have a remote server available.