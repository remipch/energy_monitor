import os
from graph_builder import GraphBuilder
from datetime import datetime, timedelta
import tempfile
import time

# Manual test for graph_builder

TEMP_DIR = tempfile.gettempdir() + '/'

CSV_PATH_1 = TEMP_DIR + "2023-12-01.csv"
CSV_PATH_2 = TEMP_DIR + "2023-12-02.csv"

IMAGE_PATH = TEMP_DIR + "test_graph_builder.svg"
print("IMAGE_PATH : ", IMAGE_PATH )

if os.path.isfile(CSV_PATH_1 ):
    os.remove(CSV_PATH_1 )

if os.path.isfile(CSV_PATH_2 ):
    os.remove(CSV_PATH_2 )

if os.path.isfile(IMAGE_PATH ):
    os.remove(IMAGE_PATH )

graph_builder = GraphBuilder(
    TEMP_DIR,
    100,
    ["a", "b"],
    ["AAA", "BB"],
    IMAGE_PATH,
    "My Title",
    "my y axis",
    "%H:%M:%S",
    timedelta(minutes=1))

# day 1
csv_1 = open(CSV_PATH_1, 'a')
csv_1.write("hour,minute,second,a,b\n");
csv_1.write("15,45,22,12,13\n")
csv_1.flush()
graph_builder.update(datetime(2023,12,1,15,45,22))
time.sleep(2)

csv_1.write("15,45,25,13,14\n")
csv_1.flush()
graph_builder.update(datetime(2023,12,1,15,45,26))
time.sleep(2)

csv_1.write("15,45,30,12,13\n")
csv_1.flush()
graph_builder.update(datetime(2023,12,1,15,45,30))
time.sleep(2)

# day 2
csv_2 = open(CSV_PATH_2, 'a')
csv_2.write("hour,minute,second,a,b\n");
csv_2.write("0,12,14,21,22\n")
csv_2.flush()
graph_builder.update(datetime(2023,12,2,0,12,15))
time.sleep(2)

csv_2.write("0,12,25,10,10\n")
csv_2.flush()
graph_builder.update(datetime(2023,12,2,0,12,28))
time.sleep(2)

csv_2.write("0,12,35,11,12\n")
csv_2.flush()
graph_builder.update(datetime(2023,12,2,0,12,38))
time.sleep(2)
