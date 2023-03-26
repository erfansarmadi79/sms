#!/bin/bash

interface=$1


sudo sed -i '/config_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/routes_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/dns_servers_'$interface'=/d' /etc/conf.d/net

# Update network configuration file with DHCP settings
echo "config_$interface=\"dhcp\"" > /etc/conf.d/net
# Restart networking service
/etc/init.d/net.eth0 restart

echo "Network configuration updated to use DHCP."

