#!/bin/bash

# Get the VGA controller info using lspci command
VGA=$(lspci | grep VGA)

# Get the vendor and device ID from the VGA controller info
VENDOR=$(echo $VGA | awk '{print $5}')
DEVICE=$(echo $VGA | awk '{print $6}')

# Print out the graphics info and memory
echo "\"graphic\": {"
echo "\"Graphics Vendor\": \"$VENDOR\","
echo "\"Graphics Device\": \"$DEVICE\""
echo "      }"
