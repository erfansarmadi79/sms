#!/bin/sh

#set -x 



interface=$1

if /sbin/ethtool "$interface" | grep -q "Link detected: yes"; then
  ip route | awk "/dev/{if(\$5==\"$interface\") print \$3}"
else
  exit 2
fi