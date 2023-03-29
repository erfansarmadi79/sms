#!/bin/sh

#set -x 



interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else
  ip route | awk "/dev/{if(\$5==\"$interface\") print \$3}"
fi

#if /sbin/ethtool "$interface" | grep -q "Link detected: yes"; then
#  ip route | awk "/dev/{if(\$5==\"$interface\") print \$3}"
#else
#  exit 2
#fi