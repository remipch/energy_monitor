from graph_builder import GraphBuilder
from datetime import datetime,timedelta
import time
import os
from pathlib import Path

# Get dir of the current python script
python_directory = Path(os.path.abspath(__file__)).parent

graph_builder = GraphBuilder(
    python_directory / "../web/data/seconds/",
    100,
    ["a0(mA)", "a1(mA)"],
    ["A0", "A1"],
    python_directory / "../web/graphs/minute.svg",
    "Last minute",
    "Current (mA)",
    "%H:%M:%S",
    timedelta(minutes=1))

print("Minute graph_builder started, waiting data from csv...")

while True:
    graph_builder.update(datetime.now())
    time.sleep(0.2)
