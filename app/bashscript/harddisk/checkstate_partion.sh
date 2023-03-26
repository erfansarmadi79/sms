#!/bin/bash

# Specify the path of the partition you want to check
PARTITION="/dev/sda2"

# Check if the partition is mounted
if grep -qs "$PARTITION" /proc/mounts; then
    # Check the read/write state of the partition
    if mount | grep -qs "$PARTITION.*(\ ro,|\ rw,)"; then
        echo "$PARTITION is mounted and writable"
    else
        echo "$PARTITION is mounted but read-only"
    fi
else
    echo "$PARTITION is not mounted"
fi

