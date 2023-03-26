#!/bin/bash

# Get the used memory and swap in kilobytes
mem_used=$(free -k | awk 'NR==2{print $3}')
swap_used=$(free -k | awk 'NR==4{print $3}')

# Convert to megabytes
mem_used_mb=$((mem_used/1024))
swap_used_mb=$((swap_used/1024))

# Display the total swap space and usage
echo "\"swap\": {"
echo "\"Total Swap\": \"$(grep SwapTotal /proc/meminfo | awk '{print $2/1024}') MB\","
echo "\"Used Swap\": \"$swap_used_mb MB\""

# Display details about each swap partition
#echo "Swap Details:"
#grep -E '^(Filename|SwapTotal|SwapFree)' /proc/swaps | awk '{ printf "%-20s %8d MB\n", $1, $3/256 }'


echo "     }"
