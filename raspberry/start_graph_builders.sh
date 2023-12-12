#!/bin/bash

# usage:

# start only hour_graph_builder :
# start_graph_builders.sh

# start hour_graph_builder and minute_graph_builder :
# start_graph_builders.sh -m

script_dir=$(dirname "$0")

pid_file=$script_dir/graph_builder_pid.txt

$script_dir/stop_graph_builders.sh

if [ "$1" == "-m" ]
then
    python3 $script_dir/python/minute_graph_builder.py &
fi

python3 $script_dir/python/hour_graph_builder.py &

echo $(jobs -p) > $pid_file
