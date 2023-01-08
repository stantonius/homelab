#!/bin/bash
echo 'GUEST HOOK: ' $*
if [ "$2" == 'post-start' ]
then

    # awk '$1=="PermitRootLogin"{foundLine=1; print "PermitRootLogin yes"} $1!="PermitRootLogin"{print $0} END{if(foundLine!=1) print "PermitRootLogin yes"}' /etc/ssh/sshd_config > /etc/ssh/sshd_config.tmp && mv /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config
    sed -e 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config > /etc/ssh/sshd_config.tmp && mv -f /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config
    
    # Restart sshd
    service ssh restart
fi