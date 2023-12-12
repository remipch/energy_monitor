#!/bin/bash

script_dir=$(dirname "$0")

pid_file=$script_dir/http_servers_pid.txt

if [ -f "$pid_file" ]; then
    kill $(cat "$pid_file")
    rm "$pid_file"
fi