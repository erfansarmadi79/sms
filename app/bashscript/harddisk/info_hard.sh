#!/bin/bash



echo "{"
echo "\"hard_disks\": ["

lsblk -J -o NAME,SIZE,MOUNTPOINT,FSTYPE,MODEL,VENDOR,STATE,TYPE | jq '.blockdevices[] | select(.type == "disk" or .type == "part")'

echo "]"
echo "}"
