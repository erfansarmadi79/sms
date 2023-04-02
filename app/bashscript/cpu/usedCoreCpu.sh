#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the status of each CPU core.
Requirements :
To run this script, you need to install Sysstat.
How to use:
The name of the script"
  exit 0
fi

# Get the number of processor cores
CORES=$(nproc)

# Print header
echo "\"CPU Core Usage\": {"

# Loop through each processor core
for ((i=0; i<$CORES; i++)); do
  # Get CPU usage stats for the core
  CORE_USAGE=$(mpstat -P $i 1 1 | awk '/Average:/ {print 100 - $NF}' | sed 's/100//g' | sed ':a;N;$!ba;s/\n/ /g')


  # Print the core usage
  echo "\"Core $i\": \"$CORE_USAGE%\"",
done

echo "       }"

