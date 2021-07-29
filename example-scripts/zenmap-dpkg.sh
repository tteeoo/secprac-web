#!/bin/bash
# removing zenmap 3
package="zenmap"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' "$package" | grep "install ok installed")
if [ "$PKG_OK" = "" ]; then
	echo "FIXED"
fi
