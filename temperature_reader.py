import time

while 1:
    with open('/sys/bus/w1/devices/28-800000282522/w1_slave') as device:
        reading = device.read()
    temp_data = reading.split('\n')[1].split(" ")[9]
    temp = float(temp_data[2:]) / 1000
    print(temp)

    time.sleep(1)
