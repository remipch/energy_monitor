#!/bin/bash

script_dir=$(dirname "$0")

$script_dir/stop_data_recorder.sh
$script_dir/stop_graph_builders.sh
$script_dir/stop_http_servers.sh
