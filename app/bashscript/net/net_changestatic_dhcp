#!/bin/bash


set -e

# Show help message if user provides -h or --help option
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Description :
This script is for changing IP interface to DHCP.

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

sudo sed -i '/config_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/routes_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/dns_servers_'$interface'=/d' /etc/conf.d/net

# Update network configuration file with DHCP settings
echo "config_$interface=\"dhcp\"" > /etc/conf.d/net
# Restart networking service
/etc/init.d/net."$interface" restart

echo "Network configuration updated to use DHCP."

fi

