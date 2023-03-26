#!/bin/bash

# Get a list of block devices with partitions
devices=$(lsblk -d -n -o NAME -e 7)

# Loop through each device and extract information about its partitions
for dev in $devices
do
    echo "Device: /dev/$dev"

    # Get information about each partition on the device
    partitions=$(lsblk "/dev/$dev")
    while read -r name fstype mountpoint size
    do
        echo "  Partition: /dev/$name"
        echo "    File system: $fstype"
        echo "    Size: $mountpoint"
	echo "    Size: $size"
        
        # Check if the partition is mounted and get its usage statistics
        if [ ! -z "$mountpoint" ] && [ "$mountpoint" != " " ]; then
            usage=$(df -Th --output=used,avail,pcent "$mountpoint" | tail -n 1)
            echo "    Mount point: $mountpoint"
            echo "    Usage: $usage"
        else
            echo "    Mount point: not mounted"
        fi
    done <<< "$partitions"

    echo
done

