#!/bin/bash

interface=$1


sudo rc-service net.$interface stop
sudo rc-update add net.$interface default
