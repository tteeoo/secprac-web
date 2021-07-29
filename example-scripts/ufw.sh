#!/bin/bash
# enabling the firewall 3
out=$(ufw status)
if [ "$out" = "Status: active" ] ; then
	echo "FIXED"
fi
