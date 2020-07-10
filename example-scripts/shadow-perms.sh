#!/bin/bash
# insecure file permissions for /etc/shadow 2
# shadow-perms-setup.sh
p=$(stat -c '%a' /etc/shadow)
[ "$p" = "600" ] && echo "FIXED"
