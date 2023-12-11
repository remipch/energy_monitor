import os
from graph_builder import GraphBuilder
from datetime import datetime, timedelta
import tempfile

IMAGE_PATH = tempfile.gettempdir()+"/test_graph_builder.svg"
print("IMAGE_PATH : ", IMAGE_PATH )

if os.path.isfile(IMAGE_PATH ):
    os.remove(IMAGE_PATH )

graph_builder = GraphBuilder(
    IMAGE_PATH,
    "My Title",
    "my y axis",
    ["Data 0", "Data 1", "Data 2"],
    "%H:%M:%S",
    timedelta(minutes=2))

now = datetime(2023,12,10,15,47,12)
graph_builder.add(datetime(2023,12,10,15,45,22), [10,10,10]) # too old: will be skiped
graph_builder.add(datetime(2023,12,10,15,47,31), [12,13,14])
graph_builder.add(datetime(2023,12,10,15,47,38), [13,14,15])
graph_builder.add(datetime(2023,12,10,15,48,25), [12,13,14])
graph_builder.add(datetime(2023,12,10,15,49,11), [13,13,13])
exit()
