#!/bin/bash
# removing user borg 4
user="borg"
id "$user" > /dev/null 2>&1 || echo "FIXED"
