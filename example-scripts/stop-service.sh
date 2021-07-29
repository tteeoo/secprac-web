#!/bin/bash
# stopping vsftpd 5
service="$vsftpd"
if ! (systemctl is-active --quiet "$service") ; then
	echo "FIXED"
fi
