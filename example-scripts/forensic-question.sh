#!/bin/bash
# answering forensic question 1 6
answer="1009"
file="/home/$SECPRAC_USER/Desktop/forensic-question-1.txt"
if grep "$answer" "$file" > /dev/null 2>&1 ; then
	echo "FIXED"
fi
