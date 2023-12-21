from graph_builder import GraphBuilder
from datetime import datetime,timedelta
import time
import os
from pathlib import Path

# Get dir of the current python script
python_directory = Path(os.path.abspath(__file__)).parent

graph_builder = GraphBuilder(
    python_directory / "../web/data/minutes/",
    100,
    ["a0(mA)", "a1(mA)"],
    ["A0", "A1"],
    python_directory / "../web/graphs/hour.svg",
    "Last hour",
    "Current (mA)",
    "%H:%M",
    timedelta(hours=1))

print("Hour graph_builder started, waiting data from csv...")

while True:
    graph_builder.update(datetime.now())
    time.sleep(1)
