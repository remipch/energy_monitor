
# This file is for debug purpose only

import serial

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

while True:
    line = ser.readline().decode("utf-8")
    print(line, end="")
    if(line.startswith("# Ready")):
        break

ser.write(b'r500')

for i in range(100):
    line = ser.readline().decode("utf-8")
    print(line, end="")

