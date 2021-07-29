#!/bin/bash
# enable firewall 3
out=$(ufw status)
if [ "$out" = "Status: active" ] ; then
	echo "FIXED"
fi
