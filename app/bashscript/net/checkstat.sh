#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script is for displaying whether the interface is active or inactive, which displays the status in the form of a message.

How to use:
Script name + interface name

tip :
If the interface name does not exist, it displays an appropriate message and returns the exitcode 2."
  exit 0
fi

# Prompt the user for a network interface name
interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else

# Use the ip link command to check whether the interface is enabled or disabled
if ip link show $interface | grep -q "state UP"; then
    echo "$interface is enabled"
else
    echo "$interface is disabled"
fi

fi