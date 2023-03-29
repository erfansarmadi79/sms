#!/bin/bash

interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else

  sudo rc-service net.$interface stop
  sudo rc-update del net.$interface default

fi

