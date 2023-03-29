#!/bin/bash

interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else

  if [[ $(cat /etc/conf.d/net | grep -c 'config_"$interface"="dhcp"') -eq 1 ]]; then
    echo "The network is configured with dynamic IP address."
  else
    echo "The network is configured with static IP address."
  fi

fi

