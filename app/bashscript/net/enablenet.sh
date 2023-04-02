#!/bin/bash

set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "
Description :
This script is for enabling the interface.

Requirements :
This script must be executed with the sudo command.

How to use:
Script name + interface name

tip :
If the interface name does not exist, it displays an appropriate message and returns the exitcode 2."
  exit 0
fi


interface=$1

if [[ ! "$(ip link show ${interface} 2> /dev/null)" ]]; then
  echo "Interface do not: ${interface}"
  exit 2
else

  sudo rc-service net.$interface start
  sudo rc-update add net.$interface default

fi