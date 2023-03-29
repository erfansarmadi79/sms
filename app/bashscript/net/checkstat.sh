#!/bin/bash

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
