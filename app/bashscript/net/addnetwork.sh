#!/bin/bash

interface=$1

ln -s /etc/init.d/net.lo /etc/init.d/net.$interface

rc-update add net.$interface default

rc-service net.$interface start
