from graph_builder import GraphBuilder
from datetime import datetime,timedelta
import time

graph_builder = GraphBuilder(
    "web/data/minutes/",
    100,
    ["a0(mA)", "a1(mA)"],
    ["A0", "A1"],
    "web/graphs/hour.svg",
    "Last hour",
    "Current (mA)",
    "%H:%M",
    timedelta(hours=1))

while True:
    graph_builder.update(datetime.now())
    time.sleep(1)
