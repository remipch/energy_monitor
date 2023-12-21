#!/bin/bash

script_dir=$(dirname "$0")

folder=$script_dir/web
port=8000

# Ugly hack to wait for the wifi to be up
sleep 5

ip_address=$(hostname -I | awk '{print $1}')

python3 -u -m http.server -d $folder --bind $ip_address $port

read -p "Press enter to close"
