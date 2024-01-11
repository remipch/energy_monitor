from build_graph import build_graph
from datetime import datetime,timedelta
import time
import os
from pathlib import Path

# Get dir of the current python script
python_directory = Path(os.path.abspath(__file__)).parent

build_graph(
    python_directory / "../web/data/minutes/",
    100,
    ["a0(mA)", "a1(mA)"],
    ["A0", "A1"],
    python_directory / "../web/graphs/hour.svg",
    "Last hour",
    "Current (mA)",
    "%H:%M",
    timedelta(hours=1))

