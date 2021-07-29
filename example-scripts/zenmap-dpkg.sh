#!/bin/bash
# remove zenmap 3
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' zenmap | grep "install ok installed")
if [ "$PKG_OK" -ne "" ]; then
	echo "FIXED"
fi
