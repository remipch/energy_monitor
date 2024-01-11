#!/bin/bash

# Note: doing the while loop in python leads to out of memory error because
# it's not possible to completely clear matplotlib memory after graph creation

# Workarround : doing the while loop in bash guaranties to free all memory
# for each graph creation (slow but it works)

while true; do
  python3 -u /home/pi/energy_monitor/raspberry/python/build_minute_graph.py

  if [ $? -ne 0 ]; then
    read -p "Press enter to close"
    break
  fi
done

