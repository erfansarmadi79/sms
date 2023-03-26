#!/bin/bash

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

