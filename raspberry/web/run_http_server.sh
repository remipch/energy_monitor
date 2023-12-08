#!/bin/bash

script_dir=$(dirname "$0")

python3 -m http.server -d $script_dir --bind 192.168.1.25 8000
