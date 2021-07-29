#!/bin/bash
# setting secure file permissions for /etc/shadow 5
# shadow-perms-setup.sh
p=$(stat -c '%a' /etc/shadow)
[ "$p" = "600" ] && echo "FIXED"
