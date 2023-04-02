#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the list of system hard disks along with their model.

How to use:
name script"
  exit 0
fi

# Get the names of all hard drives
drive_names=($(lsblk -o NAME,TYPE -p -n | grep 'disk' | awk '{print $1}'))

# Loop through each hard drive and get its model
for drive_name in "${drive_names[@]}"
do
  drive_model=$(lsblk -d -o MODEL "$drive_name")
  echo "Drive Name: $drive_name"
  echo "Drive Model: $drive_model"
  echo
done

