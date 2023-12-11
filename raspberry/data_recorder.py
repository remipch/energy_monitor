
# pip install pyserial

import serial
import csv
from data_file import DataFile
from graph_builder import GraphBuilder
from datetime import datetime, timedelta
import os

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)


# Wait arduino startup
while True:
    line = ser.readline().decode("utf-8")
    print(line, end="")
    if(line.startswith("# Ready")):
        break

# From A6 to A0: coeffs from mV to mA
# depends on transformer ratio and burden resistor
MEASURE_COEF = [30, 30, 30, 30, 30, 30, 30]

SECONDS_DIRECTORY = 'web/data/seconds/'
SECONDS_HEADER = ["hour", "minute", "second", "a6(mA)", "a5(mA)", "a4(mA)", "a3(mA)", "a2(mA)", "a1(mA)", "a0(mA)"]
SECONDS_MAX_SIZE_BYTES = 20000000 # 20 MB

MINUTES_DIRECTORY = 'web/data/minutes/'
MINUTES_HEADER = ["hour", "minute", "a6(mA)", "a5(mA)", "a4(mA)", "a3(mA)", "a2(mA)", "a1(mA)", "a0(mA)"]
MINUTES_MAX_SIZE_BYTES = 2000000000 # 2 GB

# Minutes measure is the average of all seconds measure if there is enough measure to be meaningful
# (10 s loss per minute is accepted)
MINUTES_MIN_MEASURES_COUNT = 10

LAST_MINUTE_IMAGE_PATH = "web/graphs/minute.svg"

seconds_file = DataFile(SECONDS_DIRECTORY, SECONDS_HEADER, SECONDS_MAX_SIZE_BYTES)

minutes_file = DataFile(MINUTES_DIRECTORY, MINUTES_HEADER, MINUTES_MAX_SIZE_BYTES)

last_minute_graph = GraphBuilder(
    LAST_MINUTE_IMAGE_PATH,
    "Last minute",
    "Current (mA)",
    ["A0", "A1", "A2"],
    "%H:%M:%S",
    timedelta(minutes=1))

previous_minute_time = None
minute_measures_ma = []

ser.write(b'r1000')

while(True):
    now = datetime.now()

    line = ser.readline().decode("utf-8")
    if len(line)==0:
        continue

    if line.startswith("#"):
        print(line, end="")
        continue

    # Compute and record previous minute average if minute just changed
    minute_time = now.replace(second=0, microsecond=0)
    if minute_time!=previous_minute_time and len(minute_measures_ma) >= MINUTES_MIN_MEASURES_COUNT:
        minute_average_ma = [int(sum(meas)/len(meas)) for meas in zip(*minute_measures_ma)]
        all_fields = [previous_minute_time.hour, previous_minute_time.minute] + minute_average_ma
        print("Add minute: ", all_fields)
        print("minute_measures_ma: ", minute_measures_ma)

        minutes_file.write(previous_minute_time, all_fields)
        minute_measures_ma = []
    previous_minute_time = minute_time

    print('#', line, end="")

    # Record current second
    fields = line.split()
    measure_mv = [fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]]
    measure_ma = [int(k*float(mv)) for mv, k in zip(measure_mv, MEASURE_COEF)]
    all_fields = [now.hour, now.minute, now.second] + measure_ma
    print("Add second: ", all_fields)
    seconds_file.write(now, all_fields)

    # Update last minute graph
    last_minute_graph.add(now, [measure_ma[4], measure_ma[5], measure_ma[6]])

    # Store current second in minute
    minute_measures_ma.append(measure_ma)
