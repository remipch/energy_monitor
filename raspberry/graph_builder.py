
# pip install pyserial

import serial
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import sys
import random
import shutil

TMP_PATH = 'web/graphs/tmp.svg'
OUT_PATH = 'web/graphs/minute.svg'
TIME_SPAN = timedelta(minutes=1)
SIMU = True # True False
MAX_ARRAY_LEN = 200

fig, ax = plt.subplots(figsize=(4, 6))
plt.title('Last minute')
plt.xlabel('Time')
plt.ylabel('Voltage (mV)')

time = []
voltage = []

graph, = ax.plot(time, voltage)

def update():
    global time, voltage

    if len(time)<2:
        return

    if len(time)>MAX_ARRAY_LEN:
        remove_count = len(time) - MAX_ARRAY_LEN
        time = time[remove_count:]
        voltage = voltage[remove_count:]

    max_time = max(time)
    min_time = max_time - TIME_SPAN
    mid_time = min_time + (max_time - min_time) / 2
    xticks = [min_time, mid_time, max_time]
    xlabels = [x.strftime("%H:%M:%S") for x in xticks] # for dates: "%Y-%m-%d"
    ax.set_xticks(xticks, labels=xlabels)
    ax.set_xlim(min_time, max_time)
    graph.set_data(time, voltage)

    ax.relim()
    ax.autoscale_view(scaley=True, scalex=False)
    fig.canvas.draw()

    # write in a temp file and quick copy to output to avoid temporary broken file
    fig.savefig(TMP_PATH)
    shutil.copy(TMP_PATH, OUT_PATH)

if SIMU:
    for i in range(300):
        now = datetime.now()
        print(now)
        time.append(now)
        voltage.append(random.randint(1,10))
        update()

else:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

    while True:
        line = ser.readline().decode("utf-8")
        print(line, end="")
        if(line.startswith("# Ready")):
            break

    ser.write(b'r1000')

    for i in range(1000):
        line = ser.readline().decode("utf-8")
        if len(line)==0:
            continue

        if line.startswith("#"):
            print(line, end="")
            continue

        numbers = [int(num) for num in line.split()]
        print(numbers)

        now = datetime.now()
        time.append(now)
        voltage.append(numbers[7])
        update()

    ser.write(b' ')
