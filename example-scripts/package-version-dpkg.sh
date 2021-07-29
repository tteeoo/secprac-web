#!/bin/bash
# updating firefox 3
version="Mozilla Firefox 68.9.0esr"
check="firefox --version"
if [ "$($check)" != "$version" ] ; then
	echo "FIXED"
fi
