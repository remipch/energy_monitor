#!/bin/bash

# Wait for data_recorder to eventually fix problem in input data file
sleep 10s

while true; do
  python3 -u /home/pi/energy_monitor/raspberry/python/build_hour_graph.py

  if [ $? -ne 0 ]; then
    read -p "Press enter to close"
    break
  fi

  sleep 10s
done
