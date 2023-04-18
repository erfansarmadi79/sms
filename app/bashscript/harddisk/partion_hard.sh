#!/bin/bash

# Get a list of block devices with partitions
devices=$(lsblk -d -n -o NAME -e 7)

# Count the number of partitions for each device
total_partitions=0
for dev in $devices
do
    partitions=$(lsblk -n -o NAME "/dev/$dev" | wc -l)
    total_partitions=$((total_partitions + partitions - 1))
done

# Print the total number of partitions
echo "Total partitions: $total_partitions"
