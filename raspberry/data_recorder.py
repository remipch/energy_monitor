
# pip install pyserial

import serial
import csv
from data_file import DataFile
from datetime import datetime
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

SECONDS_PATH_PREFIX = 'web/data/seconds/'
SECONDS_HEADER = ["hour", "minute", "second", "a6(mA)", "a5(mA)", "a4(mA)", "a3(mA)", "a2(mA)", "a1(mA)", "a0(mA)"]

seconds_file = DataFile(SECONDS_PATH_PREFIX, SECONDS_HEADER)

ser.write(b'r1000')

for i in range(100):
    now = datetime.now()

    line = ser.readline().decode("utf-8")
    if len(line)==0:
        continue

    if line.startswith("#"):
        print(line, end="")
        continue

    print('#', line, end="")

    date_fields = [now.hour, now.minute, now.second]
    fields = line.split()
    measure_mv = [fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]]
    measure_ma = [int(k*float(mv)) for mv, k in zip(measure_mv, MEASURE_COEF)]

    all_fields = date_fields + measure_ma
    print(all_fields)
    seconds_file.write(now, all_fields)
