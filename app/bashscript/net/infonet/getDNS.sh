#!/bin/sh

#set -x 



FILE=/etc/resolv.conf
if [ -f "$FILE" ]; then

    grep "^nameserver" /etc/resolv.conf | awk '{print $2}'

else
    exit 2
fi

#INTERFACE=$1
#
#DNS_SERVERS=$(nmcli dev show $INTERFACE | grep 'IP4.DNS' | awk '{print $2}')
#
#echo "$DNS_SERVERS"