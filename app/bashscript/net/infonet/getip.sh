#!/bin/sh

#set -x 


interface_name=$1


if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else
  ip addr show $interface_name | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1
fi

#if /sbin/ethtool "$interface_name" | grep -q "Link detected: yes"; then
#  ip addr show $interface_name | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1
#else
#  exit 2
#fi


