#!/bin/sh

#set -x 


interface=$1

if /sbin/ethtool "$interface" | grep -q "Link detected: yes"; then
  ifconfig $interface | awk '/netmask/ { print $4 }'
else
  exit 2
fi


