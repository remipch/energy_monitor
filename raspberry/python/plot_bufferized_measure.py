# This file is for debug purpose only

import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import serial
from io import StringIO
import pandas as pd


# Exit application when escape key is pressed
def on_key(event):
   if event.key == 'escape':
       sys.exit(0)
plt.gcf().canvas.mpl_connect('key_press_event', on_key)


# Open serial comm with arduino
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
while True:
    line = ser.readline().decode("utf-8")
    print(line, end="")
    if(line.startswith("# Ready")):
        break

# Config custom spearator (to output csv) and start measure
ser.write(b's,\n')
ser.write(b'b3\n')

# Read a predefined number of lines, it depends on the input_mask
# previously sent because it defines the sampling period
all_lines = ""
for i in range(200):
    line = ser.readline().decode("utf-8")
    print(line, end="")
    if not line.startswith("# "):
        all_lines = all_lines + line

# Convert to data_frame with time column in milliseconds
data = pd.read_csv(StringIO(all_lines))
data['time(ms)'] = data['#time(us)'] / 1000.0

# Plot all columns but the 'time' ones
column_names = data.columns.tolist()
for column in column_names[:]: 
    if column.startswith("A"):
      plt.plot(data['time(ms)'], data[column], label=column.replace("(mV)",""))
plt.legend(loc='best')
plt.xlabel('Time(ms)')
plt.ylabel('Voltage(mV)')
plt.show()

