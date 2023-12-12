from graph_builder import GraphBuilder
from datetime import datetime,timedelta
import time

graph_builder = GraphBuilder(
    "web/data/seconds/",
    100,
    ["a0(mA)", "a1(mA)"],
    ["A0", "A1"],
    "web/graphs/minute.svg",
    "Last minute",
    "Current (mA)",
    "%H:%M:%S",
    timedelta(minutes=1))

while True:
    graph_builder.update(datetime.now())
    time.sleep(0.2)
