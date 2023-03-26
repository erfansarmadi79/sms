#!/bin/bash

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

