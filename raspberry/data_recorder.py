
# pip install pyserial

import serial
import csv
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

SECONDS_PATH = 'web/data/today.csv'
previous_date = None
seconds_file = None
seconds_writer = None

def openSecondsFile():
    global seconds_file, seconds_writer

    must_write_header = not os.path.isfile(SECONDS_PATH)

    print("Open file")
    seconds_file = open(SECONDS_PATH, 'a', newline='')
    seconds_writer = csv.writer(seconds_file)
    if must_write_header:
        print("Write header")
        date_header = ["year", "month", "day", "hour", "minute", "second"]
        measure_header = ["a6(mA)", "a5(mA)", "a4(mA)", "a3(mA)", "a2(mA)", "a1(mA)", "a0(mA)"]
        seconds_writer.writerow(date_header + measure_header)

def readSecondsFileDate():
    with open(SECONDS_PATH, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
        if len(line)<2:
            return datetime(0)
        first_line = lines[1]
        date = datetime(int(first_line[0]), int(first_line[1]), int(first_line[2])).date()
        print("Date from existing file: ", date)
        return date

# Update the file depending on current day :
# - test if day has just changed
# - open or create file
# - write header eventually
def udpateSecondsFile(now):
    global previous_date, seconds_file

    if not os.path.isfile(SECONDS_PATH):
        # File does not exist: open and write header
        print("No existing file: create new file")
        openSecondsFile()

    elif seconds_file is None:
        # File is not yet open: read the date of the existing file
        last_date = readSecondsFileDate()

        # Close and delete today file if we just changed day
        if now.date() == last_date:
            print("Same date than existing file: keep current file")
        else:
            print("Different date than existing file: delete current file")
            os.remove(SECONDS_PATH)

        # Open file
        openSecondsFile()

    elif now.date() != previous_date:
        # Close and delete today file if we just changed day
        print("New day: close and delete current file")
        seconds_file.close()
        os.remove(SECONDS_PATH)

        # Open file
        openSecondsFile()

    previous_date = now.date()

ser.write(b'r1000')

for i in range(100):
    now = datetime.now()
    udpateSecondsFile(now)

    line = ser.readline().decode("utf-8")
    if len(line)==0:
        continue

    if line.startswith("#"):
        print(line, end="")
        continue

    print('#', line, end="")

    date_fields = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    fields = line.split()
    measure_mv = [fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]]
    measure_ma = [int(k*float(mv)) for mv, k in zip(measure_mv, MEASURE_COEF)]

    all_fields = date_fields + measure_ma
    print(all_fields)
    seconds_writer.writerow(all_fields)
    seconds_file.flush()
