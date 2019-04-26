import datetime
import os
import time

from gpiozero import LED

DATA_PATH = '/home/pi/watering/plant_data/'
pump = LED(17)


while True:
    files = os.listdir(DATA_PATH)
    files.sort(key = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d.txt'))
    newest_file_name = files[-1]
    f = open(DATA_PATH+newest_file_name, 'r')
    lines = f.read().splitlines()
    last_line = lines[-1]
    dryness = int(last_line.strip().split('\t')[1])
    print("Plant is at dryness %s" % dryness)
    hour = int(time.strftime("%H"))
    #Don't turn on the pump at night.
    if dryness > 600 and (hour < 21 and hour > 9):
        print("Needs water! Pumping for 1 second.")
        pump.on()
        time.sleep(1)
        pump.off()
    time.sleep(121)
