#!/bin/bash

set -e

# Get list of network interfaces
interfaces=$(ip link show | awk -F': ' '{print $2}' | grep -v lo)

# Initialize variables to store up and down interfaces
up_interfaces=""
down_interfaces=""

# Loop through each interface and check its status
for interface in $interfaces
do
    status=$(ip link show $interface | grep -o 'state [A-Z]\+' | awk '{print $2}')
    if [ $? -eq 0 ]
    then
        if [ "$status" == "UP" ]
        then
            up_interfaces="$up_interfaces $interface \n "
        elif [ "$status" == "DOWN" ]
        then
            down_interfaces="$down_interfaces $interface \n "
        fi
    else
        echo "Error getting status for $interface"
    fi
done

# Print list of up interfaces
echo "Up interfaces:"
echo -e "$up_interfaces"

# Print list of down interfaces
echo "Down interfaces:"
echo -e "$down_interfaces"

