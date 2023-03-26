#!/bin/bash


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






