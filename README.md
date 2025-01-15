# ArduinoControlAudio


The main program is "ControlAudioDevice+Volume.py". It reads values from the serial input of an arduino and performs according actions through [nircmd](https://www.nirsoft.net/utils/nircmd.html).

Incoming values are from an ultrasound distance sensor(0-500, distance in cm) 
or from a potentiometer(1000-1100, percent).

The distance read from the sensor controls the system audio device.
The read values from the poti control the system volume.

<img src="https://github.com/user-attachments/assets/3d453d00-7506-40fc-a8d7-a8cec06f9764" width="400" />
