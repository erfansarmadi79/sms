#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the status of the memory, such as: the amount of consumption and the available amount, etc.

Those in need:
To run this script, you need to install dmidecode.
And to run this script, you need sudo.

How to use:
The name of the script"
  exit 0
fi


# Get total memory available
total_mem=$(free -h | awk '/^Mem:/{print $2}' | sed 's/i//g')

# Get used memory
used_mem=$(free -h | awk '/^Mem:/{print $3}' | sed 's/i//g')

# Get free memory
free_mem=$(free -h | awk '/^Mem:/{print $4}' | sed 's/i//g')

# Get shared memory
shared_mem=$(free -h | awk '/^Mem:/{print $5}' | sed 's/i//g')

# Get cached memory
cached_mem=$(free -h | awk '/^Mem:/{print $6}' | sed 's/i//g')

# Get available memory
available_mem=$(free -h | awk '/^Mem:/{print $7}' | sed 's/i//g')

# Get memory module information
memory_info=$(sudo dmidecode --type memory | grep "Manufacturer" | awk '{print $2}' | sed '/Not/d')



# Print memory details
echo "\"memory\"; {"
echo "\"Memory Module Name\": \"$memory_info\","
echo "\"Total memory\": \"$total_mem\","
echo "\"Used memory\": \"$used_mem\","
echo "\"Free memory\": \"$free_mem\","
echo "\"Shared memory\": \"$shared_mem\","
echo "\"Cached memory\": \"$cached_mem\","
echo "\"Available memory\": \"$available_mem\","
echo "     }"

