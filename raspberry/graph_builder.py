
# pip install pyserial

import serial
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import sys
import random

# SIMU = True
SIMU = False
MAX_ARRAY_LEN = 200

# Exit application when escape key is pressed
def on_key(event):
   if event.key == 'escape':
       sys.exit(0)

fig, ax = plt.subplots(figsize=(4, 6))
fig.canvas.mpl_connect('key_press_event', on_key)
ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=1, maxticks=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.title('Voltage (mV)')
plt.xlabel('Time')

time = []
voltage = []

graph, = ax.plot(time, voltage)

def update():
    global time, voltage
    if len(time)>MAX_ARRAY_LEN:
        remove_count = len(time) - MAX_ARRAY_LEN
        time = time[remove_count:]
        voltage = voltage[remove_count:]
    graph.set_data(time, voltage)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.savefig("web/graphs/day.svg", transparent=True)
    plt.pause(0.001)

if SIMU:
    for i in range(30):
        update()
        for j in range(10):
            now = datetime.now()
            time.append(now)
            voltage.append(random.randint(1,10))
            plt.pause(0.05)

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
