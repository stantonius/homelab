#!/bin/bash

# Logging the start of script
echo "$(date) - Hook script started" >> /tmp/hookscript.log

echo "$(date) - GUEST HOOK: " $* >> /tmp/hookscript.log 2>&1

if [ "$2" == 'post-start' ]
then

    # Logging before modifying sshd_config
    echo "$(date) - Modifying sshd_config" >> /tmp/hookscript.log

    # Uncomment the PermitRootLogin configuration
    sed -e 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config > /etc/ssh/sshd_config.tmp && mv -f /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config

    # Logging before restarting ssh service
    echo "$(date) - Restarting ssh service" >> /tmp/hookscript.log

    # Restart sshd
    service ssh restart

    # Logging after ssh service restart
    echo "$(date) - SSH service restarted" >> /tmp/hookscript.log

fi

# Logging the end of script
echo "$(date) - Hook script ended" >> /tmp/hookscript.log
