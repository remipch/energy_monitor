from build_graph import build_graph
from datetime import datetime,timedelta
import time
import os
from pathlib import Path

# Get dir of the current python script
python_directory = Path(os.path.abspath(__file__)).parent

build_graph(
    python_directory / "../web/data/minutes/",
    200,
    ["a0(mA)", "a1(mA)", "a2(mA)", "a3(mA)"],
    ["Conso", "PPV", "PAC", "EDF" ],
    python_directory / "../web/graphs/hour.svg",
    "Last 3 hours",
    "Current (mA)",
    "%H:%M",
    timedelta(hours=3))

