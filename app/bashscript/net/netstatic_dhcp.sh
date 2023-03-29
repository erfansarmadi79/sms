#!/bin/bash

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

