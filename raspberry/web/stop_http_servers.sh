#!/bin/bash

script_dir=$(dirname "$0")

kill $(cat $script_dir/http_servers_pid.txt)
