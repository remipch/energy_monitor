#!/bin/bash

script_dir=$(dirname "$0")

$script_dir/stop_http_servers.sh

web_interface_folder=$script_dir
web_interface_port=8000

web_data_folder=$script_dir/data
web_data_port=8001

ip_address=$(hostname -I | awk '{print $1}')

# -u option force unbuffered output
# 2>&1 output stdout and stderr
# tee duplicate to console
python3 -u -m http.server -d $web_interface_folder --bind $ip_address $web_interface_port 2>&1 | tee web_interface.log &

python3 -u -m http.server -d $web_data_folder --bind $ip_address $web_data_port 2>&1 | tee web_data.log &

echo $(jobs -p) > $script_dir/http_servers_pid.txt
