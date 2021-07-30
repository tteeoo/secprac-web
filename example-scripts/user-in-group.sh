#!/bin/bash
# making data an administrator 4
user="data"
group="sudo"
if id -nG "$user" | grep "$group" > /dev/null 2>&1 ; then
	echo "FIXED"
fi
