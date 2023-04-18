#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the status of system hard disks.
How to use:
The name of the script"
  exit 0
fi



echo "{"
echo "\"hard_disks\": ["

lsblk -J -o NAME,SIZE,MOUNTPOINT,FSTYPE,MODEL,VENDOR,STATE,TYPE | jq '.blockdevices[] | select(.type == "disk" or .type == "part")'

echo "]"
echo "}"
