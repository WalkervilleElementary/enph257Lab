#! /bin/python3
import serial
import time
from datetime import datetime
from math import ceil

period = 10 * 60 #seconds
filename = str(datetime.utcnow()).split(".")[0].replace(" ", "_") + ".csv"
out_file = open(filename, "w")

def get_time():
    return time.monotonic() - get_time.start_time
get_time.start_time = 0

with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
    get_time.start_time = time.monotonic()
    while True:
        sample_time = get_time()
        heat = True if (sample_time / period) % 1 < 0.5 else False
        ser.write(bytes(b'H' if heat else b'L'))
        raw = ser.readline()
        entries = ["{0:.3f}".format(sample_time)]
        try:
            values = list(map(str, map(int, raw.decode().replace("\n", "").split(","))))
            if len(values) != 7:
                raise Exception("Must get 7 data points per reading!")
            entries += values
        except:
            entries.append('"bad sample"')
            entries.append(str(raw))
        entries.append(1 if heat else 0)
        #print(entries)
        print("\t".join(entries))
        out_file.write(",".join(entries) + "\n")
        time.sleep(ceil(get_time()) - get_time())
