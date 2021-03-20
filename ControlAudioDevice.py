import serial
import subprocess
from time import sleep

wasBlocked = True   # True = sth is blocking the sensor -> Speakers
currentyBlocked = False
serialInput = serial.Serial(port="COM3")
counter = 0

while True:
    ser_bytes = serialInput.readline()
    decoded_int = int(ser_bytes.decode("utf-8"))
    # interpret distance; blocked if less than 15 cm away
    if decoded_int < 15:
        currentyBlocked = True
    elif decoded_int < 200:
        currentyBlocked = False
    
    print(currentyBlocked)

    if currentyBlocked and not wasBlocked:
        if counter < 3:
            counter += 1
        else:
            # only change state if value consistently changed for 3 readings
            wasBlocked = True
            print("BOXEN")
            subprocess.run("nircmd.exe setdefaultsounddevice BOXEN 1")
            counter = 0

    elif not currentyBlocked and wasBlocked:
        if counter < 3:
            counter += 1
        else:
            # only change state if value consistently changed for 3 readings
            wasBlocked = False
            print("SENNHEISER")
            subprocess.run("nircmd.exe setdefaultsounddevice SENNHEISER 1")
    else:   
        # Value didn't change
        # if counter was 1 or 2, the values were temporary outliers; counter reset
        counter = 0