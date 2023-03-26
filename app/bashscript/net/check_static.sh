#!/bin/bash

if [[ $(cat /etc/conf.d/net | grep -c 'config_eth0="dhcp"') -eq 1 ]]; then
  echo "The network is configured with dynamic IP address."
else
  echo "The network is configured with static IP address."
fi

