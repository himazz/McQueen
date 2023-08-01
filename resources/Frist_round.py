#!python3
import serial
import time

# creat arduino object
arduino = serial.Serial(port='COM14', baudrate=9600, timeout=.1)

while True:
    x = arduino.readline()
    print(x)