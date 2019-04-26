import serial
from datetime import datetime

ser = serial.Serial('/dev/ttyS0', 115200)  # open serial port
current_day = -1
f = None

while True:
    value = ser.readline().strip().decode()     # read the number
    print("Got %s from serial!" % value)
    current_epoch_time = (datetime.now() - datetime(1970,1,1)).total_seconds()
    now = datetime.now()

    f = open("plant_data/%s-%s-%s.txt" % (now.year, now.month, now.day), 'a')
    f.write("%s\t%s\n" % (current_epoch_time, value))
    f.close()



ser.close()
