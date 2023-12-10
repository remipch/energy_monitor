#!/bin/bash

script_dir=$(dirname "$0")

web_interface_folder=$script_dir
web_interface_port=8000

web_data_folder=$script_dir/data
web_data_port=8001

# -u option force unbuffered output
# 2>&1 output stdout and stderr
# tee duplicate to console
python3 -u -m http.server -d $web_interface_folder --bind 192.168.1.25 $web_interface_port 2>&1 | tee web_interface.log &
# echo $(jobs -p) > $script_dir/web_interface_pid.txt

python3 -u -m http.server -d $web_data_folder --bind 192.168.1.25 $web_data_port 2>&1 | tee web_data.log &

echo $(jobs -p) > $script_dir/http_servers_pid.txt
