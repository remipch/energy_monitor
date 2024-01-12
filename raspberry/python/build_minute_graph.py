from build_graph import build_graph
from datetime import datetime,timedelta
import time
import os
from pathlib import Path

# Get dir of the current python script
python_directory = Path(os.path.abspath(__file__)).parent

build_graph(
    python_directory / "../web/data/seconds/",
    330,
    ["a3(mA)", "a2(mA)", "a1(mA)"],
    ["BEC", "Appoint", "PAC" ],
    python_directory / "../web/graphs/minute.svg",
    "Last 5 minutes",
    "Current (mA)",
    "%H:%M:%S",
    timedelta(minutes=5))

