#!/bin/bash

script_dir=$(dirname "$0")

pid_file=$script_dir/data_recorder_pid.txt

if [ -f "$pid_file" ]; then
    kill $(cat "$pid_file")
    rm "$pid_file"
fi
