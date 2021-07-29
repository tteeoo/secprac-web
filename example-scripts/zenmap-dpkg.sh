#!/bin/bash
# removing zenmap 3
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' zenmap | grep "install ok installed")
if [ "$PKG_OK" != "" ]; then
	echo "FIXED"
fi
