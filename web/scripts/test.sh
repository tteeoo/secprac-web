#!/bin/sh
# bad file in home directory 3
# test-setup.sh
[ -f /home/$SECPRAC_USER/badfile ] || echo "FIXED"
