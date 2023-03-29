#!/bin/sh

#set -x 


interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else
  ifconfig $interface | awk '/netmask/ { print $4 }'
fi

#if /sbin/ethtool "$interface" | grep -q "Link detected: yes"; then
#  ifconfig $interface | awk '/netmask/ { print $4 }'
#else
#  exit 2
#fi


