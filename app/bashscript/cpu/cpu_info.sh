#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script displays the status of system cpu.
How to use:
The name of the script"
  exit 0
fi

echo "\"Cpuinfo\": {"
# Display the CPU model name
echo "\"CPU model name\": \"$(cat /proc/cpuinfo | grep "model name" | uniq | awk -F":" '{print $2}')\","

# Display the number of CPU cores
echo "\"Number of CPU cores\": \"$(cat /proc/cpuinfo | grep "processor" | wc -l)\","

# Display the CPU clock speed
speedClock=$(cat /proc/cpuinfo | grep "cpu MHz" | uniq | awk -F":" '{print $2}' | sed -n '$p')

echo "\"CPU clock speed\": \"$(echo "scale=2; $speedClock / 1000" | bc)GHz\","

echo "\"CPU Cash size\": \"$(lscpu | grep -i "L3 cache:" | awk '{print $3}'MB)\""

echo "   }"






