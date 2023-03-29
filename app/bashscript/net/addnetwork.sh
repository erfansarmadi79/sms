#!/bin/bash

interface=$1


if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else

  ln -s /etc/init.d/net.lo /etc/init.d/net.$interface

  rc-update add net.$interface default

  rc-service net.$interface start

fi
