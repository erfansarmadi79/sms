#!/bin/bash

#set -e

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

