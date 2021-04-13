import serial
import subprocess
from time import sleep

'''
A programm that reads values from the serial input of an arduino.
Incoming values are from an ultrasound distance sensor(0-500, distance in cm) 
or from a potentiometer(1000-1100, percent).

The distance read from the sensor controls the system audio device.
The read values from the poti control the system volume.
'''

# Helper function that scales incoming values, e.g. 0-100 to 0-65555
def translateValues(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

# Variables
wasBlocked = True   # True = sth is blocking the sensor -> Speakers
currentyBlocked = False
serialInput = serial.Serial(port="COM3")
counter = 0
oldPotiValue = 0

# initial check the get baseline
ser_bytes = serialInput.readline()
decoded_int = int(ser_bytes.decode("utf-8"))
if decoded_int < 1000:
    if decoded_int < 15:
        subprocess.run("nircmd.exe setdefaultsounddevice BOXEN 1")
    elif decoded_int < 200:
        subprocess.run("nircmd.exe setdefaultsounddevice SENNHEISER 1")

# Programm loop that consistently reads the serial input from the arduino
while True:
    ser_bytes = serialInput.readline()
    decoded_int = int(ser_bytes.decode("utf-8"))
    if decoded_int < 1000:
        # PROXIMITY VALUE
        # interpret distance; blocked if less than 15 cm away
        if decoded_int < 15:
            currentyBlocked = True
        elif decoded_int < 200:
            currentyBlocked = False

        if currentyBlocked and not wasBlocked:
            if counter < 3:
                counter += 1
            else:
                # only change state if value consistently changed for 3 readings
                wasBlocked = True
                print("Changed audio device to BOXEN")
                subprocess.run("nircmd.exe setdefaultsounddevice BOXEN 1")
                counter = 0

        elif not currentyBlocked and wasBlocked:
            if counter < 3:
                counter += 1
            else:
                # only change state if value consistently changed for 3 readings
                wasBlocked = False
                print("Changed audio device to SENNHEISER")
                subprocess.run("nircmd.exe setdefaultsounddevice SENNHEISER 1")
                counter = 0
        else:   
            # Value didn't change
            # if counter was 1 or 2, the values were temporary outliers; counter reset
            counter = 0
    else:
        # POTI VALUE
        if decoded_int <=1100:            
            percentValue = decoded_int - 1000
            difference = oldPotiValue - percentValue
            # only change if difference between old and new value is more than one
            # since poti values slightly fluctuate
            if difference < -1 or difference > 1:
                oldPotiValue = percentValue
                scaledValue = translateValues(percentValue, 0, 100, 0, 65555) # scale to 0-65555
                subprocess.run("nircmd.exe setsysvolume " + str(scaledValue))
                print("Changed volume to " + str(oldPotiValue))
        else:
            print("invalid value read: " + str(decoded_int))
