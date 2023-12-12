#!/bin/bash

script_dir=$(dirname "$0")

pid_file=$script_dir/data_recorder_pid.txt

$script_dir/stop_data_recorder.sh

python3 $script_dir/python/data_recorder.py &

echo $(jobs -p) > $pid_file
