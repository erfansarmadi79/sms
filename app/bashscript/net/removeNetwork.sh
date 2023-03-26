#!/bin/bash
sudo ifconfig eth0 down
sudo rm /etc/init.d/net.eth0
sudo rc-update del net.eth0
