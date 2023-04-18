#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the status of being or not being readonly.

How to use:
name script"
  exit 0
fi


# Check the read/write state of the partition
if mount | grep -qs "$PARTITION.*(\ ro,|\ rw,)"; then
    echo "$PARTITION is mounted and writable"
else
    echo "$PARTITION is mounted but read-only"
fi


