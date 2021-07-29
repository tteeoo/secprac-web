#!/bin/bash
# making data an administrator 4
user="data"
group="sudo"
if id -nG "$user" | grep -qw "$group" ; then
	echo "FIXED"
else
