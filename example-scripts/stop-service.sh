#!/bin/bash
# stopping vsftpd 5
service="vsftpd"
systemctl is-active --quiet "$service" || echo "FIXED"
