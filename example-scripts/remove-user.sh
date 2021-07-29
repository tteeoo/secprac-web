#!/bin/bash
# remove user borg 4
user="borg"
if ! (id "$user" &> /dev/null) ; then
	echo "FIXED"
else
